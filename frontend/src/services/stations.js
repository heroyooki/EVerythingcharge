import {request} from "@/api";
import router from "@/router";

const API_URL = import.meta.env.VITE_API_URL.trim("/");

const {currentRoute} = router;

const endpoint = "charge_points";

export function deleteStation(stationId) {
  return request.delete(
    `/${currentRoute.value.params.networkId}/${endpoint}/${stationId}`
  );
}

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
    }/${endpoint}/?${searchParams.toString()}`
  );
}

export function getStation(stationId) {
  return request.get(
    `/${currentRoute.value.params.networkId}/${endpoint}/${stationId}`
  );
}

export function updateStation(stationId, data) {
  return request.put(
    `/${currentRoute.value.params.networkId}/${endpoint}/${stationId}`,
    data
  );
}

export function updateConnector({stationId, connectorId}) {
  return request.put(
    `/${currentRoute.value.params.networkId}/${endpoint}/${stationId}/connectors/${connectorId}`
  );
}

export function softResetStation(stationId) {
  return request.patch(
    `/${currentRoute.value.params.networkId}/${endpoint}/${stationId}`
  );
}

export function downloadQRCode({stationId, connectorId}) {
  const link = document.createElement("a");
  link.href = `${API_URL}/${stationId}/connectors/${connectorId}/qrcode`;
  link.target = "_blank";

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
