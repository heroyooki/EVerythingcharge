import {ref} from "vue";
import {useStore} from "vuex";

export function useGetter({itemsLoader, callback}) {
  const item = ref({});
  const {commit} = useStore();

  const fetchData = () => {
    commit("setGlobalLoading");
    return itemsLoader()
      .then((response) => {
        item.value = response;
        if (callback !== undefined) {
          callback(item.value)
        }
      })
      .finally(() => {
        commit("unsetGlobalLoading");
      });
  };
  fetchData();
  return {item, fetchData};
}
