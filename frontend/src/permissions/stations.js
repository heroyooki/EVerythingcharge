import {STATION_STATUS} from "@/enums";

export const isForbiddenToReset = station => {
  return station.status !== STATION_STATUS.available
}
