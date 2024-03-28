export const DATETIME_FORMAT = "MMM DD, YYYY, hh:mm A";

export const STATION_STATUS = {
  available: "Available",
  unavailable: "Unavailable",
  faulted: "Faulted",
  preparing: "Preparing",
  charging: "Charging",
  suspendedEVSE: "SuspendedEVSE",
  suspendedEV: "SuspendedEV",
  finishing: "Finishing",
};

export const STATION_STATUS_COLOR = {
  available: "#8cef91",
  unavailable: "#7e817d",
  faulted: "#DC184CFF",
  preparing: "#efc909",
  charging: "#0fe018",
};

export const OPERATORS_STATUS = {
  true: "#0ee018",
  false: "#DC184CFF",
};

export const TRANSACTIONS_STATUS_COLOR = {
  in_progress: "#0fe018",
  pending: "#efc909",
  completed: "#7e817d",
  faulted: "#DC184CFF",
};

export const TRANSACTIONS_STATUS_VIEW = {
  in_progress: "mdi mdi-progress-clock",
  pending: "mdi mdi-progress-question",
  completed: "mdi mdi-progress-check",
  faulted: "mdi mdi-progress-close",
};

export const TRANSACTIONS_MAPPPER = {
  in_progress: "in progress",
  pending: "pending",
  completed: "completed",
  faulted: "faulted",
};

export const TRANSACTIONS_STATUS = {
  in_progress: "in_progress",
  pending: "pending",
  completed: "completed",
  faulted: "faulted",
};

export const ACTION_STATUS_COLOR = {
  pending: "#efc909",
  completed: "#0ee018",
  faulted: "#DC184CFF",
};

export const Role = {
  resident: "admin",
  employee: "operator",
};
