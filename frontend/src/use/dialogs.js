import { ref } from "vue";

const dialog = ref(false);

export function useConfirm() {
  const openConfirm = () => {
    dialog.value = true;
  };
  const closeConfirm = () => {
    dialog.value = false;
  };
  return { dialog, openConfirm, closeConfirm };
}
