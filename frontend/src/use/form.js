import {ref, watch} from "vue";

export function useSubmitForm({itemSender, callback}) {
  const loading = ref(false);
  const isValid = ref(false);
  const dialog = ref(false);
  const data = ref({});
  const errors = ref({});
  const showError = ref(false);

  watch(dialog, () => {
    if (!dialog.value) {
      data.value = {};
      clearError();
    }
  })

  const clearError = () => {
    showError.value = false;
    errors.value = {};
  };

  const openModal = () => {
    dialog.value = true;
  };

  const closeModal = () => {
    dialog.value = false;
  };

  const sendData = () => {
    loading.value = true;
    itemSender(data.value)
      .then((response) => {
        if (callback !== undefined) {
          callback(response)
        }
        closeModal();
      })
      .catch(({response}) => {
        showError.value = true;
        errors.value[response?.data?.key] = response?.data?.detail;
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
