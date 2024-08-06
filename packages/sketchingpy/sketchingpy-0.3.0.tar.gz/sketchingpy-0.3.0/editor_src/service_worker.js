const pendingRequests = new Map();
const CACHE_NAME = "sketchbook-cache-202405011";

const requestsChannel = new BroadcastChannel("requests");
const responsesChannel = new BroadcastChannel("responses");

const EDITABLE_FILE_TYPES = [
    ".py",
    ".pyscript",
    ".txt",
    ".json",
    ".geojson",
    ".csv"
];

const PYSCRIPT_CONFIG = {
    "packages": ["/dist/sketchingpy-0.3.0-py3-none-any.whl"]
};


function getIsEditable(name) {
    const editableExtension = EDITABLE_FILE_TYPES.filter((x) => name.endsWith(x));
    return editableExtension.length != 0;
}


function getIsSketch(request) {
    const url = new URL(request.url);
    const nakedPathName = url.pathname.replace("/", "");
    const isSketch = nakedPathName === "sketch.html";
    return isSketch;
}


function getRequiresNetwork(request) {
    const url = new URL(request.url);
    const nakedPathName = url.pathname.replace("/", "");
    const isIndex = nakedPathName === "index.html" || url.pathname === "/";
    const isSketch = nakedPathName === "sketch.html";
    const isServiceWorker = nakedPathName === "service_worker.js";
    const isWebWorker = nakedPathName === "file_worker.js";
    const isNested = url.pathname.substring(1, url.pathname.length).indexOf("/") != -1;
    const exceptions = [isIndex, isServiceWorker, isNested, isSketch, isWebWorker];
    const numExceptions = exceptions
        .filter((x) => x == true);
    return numExceptions.length > 0;
}


async function interceptRequest(request) {
    const url = new URL(request.url);
    const currentHost = self.location.hostname;

    const makeNetworkRequest = () => {
        return caches.open(CACHE_NAME).then((cache) => {
            const makeCachedRequest = () => {
                return fetch(request).then(async (networkResponse) => {
                    const isCurrentHost = url.hostname === currentHost;
                    const isResponseOk = networkResponse.ok;
                    const isGet = request.method === "GET";
                    if (isCurrentHost && isResponseOk && isGet) {
                        cache.put(url.pathname, networkResponse.clone());
                    }
                    return networkResponse;
                });
            }

            return cache.match(url.pathname).then((cachedValue) => {
                if (cachedValue !== undefined) {
                    return new Promise((resolve) => {
                        resolve(cachedValue);
                    });
                    makeCachedRequest();
                } else {
                    return makeCachedRequest();
                }
            });
        });
    }

    let future = null;
    if (currentHost !== url.hostname) {
        future = fetch(url.pathname).then(async (networkResponse) => {
            return networkResponse;
        });
    } else if (getIsSketch(request)) {
        const filenamesFuture = manager.getItemNames();
        
        const networkFuture = makeNetworkRequest()
            .then((response) => response.text());

        const combinedFutures = Promise.all([filenamesFuture, networkFuture]);

        future = combinedFutures.then((results) => {
            const filenames = results[0];
            const pageText = results[1];

            const filesObj = {};
            filenames.forEach((filename) => {
                filesObj["/" + filename] = "./" + filename;
            });
            const configObj = {
                "packages": PYSCRIPT_CONFIG["packages"],
                "files": filesObj
            };
            const configObjStr = JSON.stringify(configObj);

            const sketchFile = url.searchParams.get("filename");
            const epochTime = Date.now();
            const sketchFileCacheBuster = sketchFile + "?v=" + epochTime;

            return pageText.replace("{{{ config }}}", configObjStr)
                .replace("{{{ sketchFile }}}", sketchFileCacheBuster);
        }).then((content) => {
            const headers = {"headers": { "Content-Type": "text/html" }};
            return new Response(content, headers);
        });
    } else if (getRequiresNetwork(request)) {
        future = makeNetworkRequest();
    } else {
        const effectiveUrl = url.pathname.replace("/", "");
        future = getItem(effectiveUrl).then((content) => {
            if (getIsEditable(effectiveUrl)) {
                return new Response(content);
            } else {
                return fetch(content)
                    .then((response) => response.blob())
                    .then((blob) => new Response(blob));
            }
        });
    }

    return (await future);
}


self.addEventListener("fetch", (event) => {
    const request = event.request;
    event.respondWith(interceptRequest(request));
});


class ReadOnlyOpfsFileManager {

    constructor() {
        const self = this;
        self._waitingPromises = new Map();

        responsesChannel.onmessage = (event) => {
            const data = event.data;
            const resolve = self._waitingPromises.get(data["target"]);
            self._waitingPromises.delete(data["target"]);
            resolve(data["content"]);
        };
    }
    
    getItem(filename) {
        const self = this;
        const target = Date.now() + "." + filename;

        return new Promise((resolve) => {
            self._waitingPromises.set(target, resolve);
            requestsChannel.postMessage({
                "filename": filename,
                "target": target
            });
        });
    }

    getItemNames() {
        const self = this;
        const target = Date.now() + ".";

        return new Promise((resolve) => {
            self._waitingPromises.set(target, resolve);
            requestsChannel.postMessage({
                "filename": "",
                "target": target
            });
        });
    }
    
}


const manager = new ReadOnlyOpfsFileManager();


function getItem(path) {
    return manager.getItem(path);
}
