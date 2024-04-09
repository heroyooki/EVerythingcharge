import {request} from "@/api";
import router from "@/router";

const API_URL = import.meta.env.VITE_API_URL.trim("/");

const {currentRoute} = router;

const endpoint = "charge_points";


export function addStation(data) {
  return request.post(
    `/${currentRoute.value.params.networkId}/${endpoint}`,
    data
  );
}

export function listStations(queryParams) {
  let searchParams = new URLSearchParams(queryParams);
  return request.get(
    `/${
      currentRoute.value.params.networkId
    }/${endpoint}?${searchParams.toString()}`
  );
}

export function getStation(stationId) {
  return request.get(
    `/${currentRoute.value.params.networkId}/${endpoint}/${stationId}`
  );
}
