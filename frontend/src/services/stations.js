import {request} from "@/api";
import router from "@/router";
import store from "@/store";

const API_URL = import.meta.env.VITE_API_URL.trim("/");

const {currentRoute} = router;

const endpoint = "charge_points";


export function addStation(data) {
  // Create station
  return request.post(
    `/${currentRoute.value.params.networkId}/${endpoint}`,
    data
  )
    // Add configurations to the station
    .then(response => {
      request.post(
        `/${currentRoute.value.params.networkId}/${endpoint}/${response.id}/configurations`,
        store.getters.configurationsAsPayload
      );
      return response
    });
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
