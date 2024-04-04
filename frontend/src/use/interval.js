export function useInterval() {
  let interval = null;

  const fetchWithInterval = fetcher => interval = setInterval(() => fetcher(), 10000);
  const dropInterval = () => clearInterval(interval);

  return {fetchWithInterval, dropInterval}
}
