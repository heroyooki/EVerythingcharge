import { reactive, ref } from "vue";

export function useSubmitForm({ itemSender, afterHandler }) {
  const loading = ref(false);
  const isValid = ref(false);
  const dialog = ref(false);
  const data = reactive({});
  const errors = ref({});
  const showError = ref(false);

  const clearError = () => {
    showError.value = false;
    errors.value = {};
  };

  const openModal = () => {
    dialog.value = true;
  };

  const closeModal = () => {
    dialog.value = false;
    data.value = null;
    clearError();
  };

  const sendData = () => {
    loading.value = true;
    itemSender(data)
      .then((response) => {
        afterHandler(response);
        closeModal();
      })
      .catch(({ response }) => {
        const { data } = response;
        showError.value = true;
        errors.value[data.key] = data.detail;
      })
      .finally(() => {
        loading.value = false;
      });
  };
  return {
    loading,
    isValid,
    dialog,
    data,
    errors,
    showError,
    clearError,
    openModal,
    closeModal,
    sendData,
  };
}
