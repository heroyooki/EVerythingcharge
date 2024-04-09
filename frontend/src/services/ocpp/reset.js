import {request} from "@/api";
import router from "@/router";

const API_URL = import.meta.env.VITE_API_URL.trim("/");

const {currentRoute} = router;

const endpoint = "charge_points";

export function reset(stationId, data) {
  return request.patch(
    `/${currentRoute.value.params.networkId}/${endpoint}/${stationId}/reset`,
    data
  )
}
