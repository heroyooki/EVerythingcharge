import {request} from "@/api";
import router from "@/router";

const {currentRoute} = router;

const endpoint = "networks";

export function addNetwork(data) {
  return request.post(`/${endpoint}`, data);
}

export function listNetworks(params) {
  let searchParams = new URLSearchParams(params);
  return request.get(`/${endpoint}/?${searchParams.toString()}`);
}

export function getNetwork(networkId) {
  return request.get(`${endpoint}/${networkId}`);
}
