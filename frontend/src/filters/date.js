import moment from "moment";
import { DATETIME_FORMAT } from "@/components/enums";

function dateAgo(value) {
  if (value) {
    return moment.utc(String(value)).local().fromNow();
  }

  return "–";
}

function date(value, format = DATETIME_FORMAT) {
  if (value) {
    return moment(String(value)).local().format(format);
  }

  return "–";
}

export { date, dateAgo };
