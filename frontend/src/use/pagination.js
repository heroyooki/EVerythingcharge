import { ref, watch } from "vue";
import { useStore } from "vuex";
import { rules } from "@/configs/validation";

export function usePagination({ itemsLoader, afterHandler }) {
  const currentPage = ref(1);
  const lastPage = ref(0);
  const items = ref([]);
  const search = ref("");
  const { commit } = useStore();
  let timeout = null;

  const fetchData = (args) => {
    let query = Object.assign(
      { page: currentPage.value, search: search.value },
      args || {}
    );
    if (!query.periodic) {
      commit("setGlobalLoading");
    }
    return itemsLoader(query)
      .then((response) => {
        if (!response.items.length && currentPage.value > 1) {
          currentPage.value--;
        }
        items.value = response.items;
        lastPage.value = response.pagination.last_page;
        if (afterHandler !== undefined) {
          afterHandler(response.items);
        }
      })
      .finally(() => {
        commit("unsetGlobalLoading");
      });
  };
  fetchData();
  watch(currentPage, () => fetchData());
  watch(search, (newValue, oldValue) => {
    let newValueLength = newValue.trim().length;
    let oldValueLength = oldValue.trim().length;
    if (
      newValueLength >= rules.minLength ||
      (!newValueLength && oldValueLength)
    ) {
      clearTimeout(timeout);
      timeout = setTimeout(fetchData, 500, newValue);
    }
  });
  return { currentPage, lastPage, fetchData, items, search };
}
