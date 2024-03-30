export const validationRules = {

  id: [
    value => {
      const regex = /^[a-zA-Z0-9а-яА-Я]+$/;
      if (!regex.test(value)) {
        return "Only latin letters and numbers are allowed."
      }
      return true;
    }
  ],

  description: [
    value => {
      if (value?.length && value.length < 5) {
        return "Description must be empty or at least 5 characters long."
      }
      if (value.length > 124) {
        return "Description must be empty or at most 124 characters long."
      }
      return true
    }
  ],

  location: [
    value => {
      if (value?.length < 3) {
        return "Location must be at least 3 characters long."
      }
      if (value?.length > 48) {
        return "Location must be at most 48 characters long."
      }
      return true
    }
  ],

  ocpp_version: [
    value => {
      if (!(value === "1.6" || value === "2.0.1")) {
        return "OCPP Version must be 1.6 or 2.0.1"
      }
      return true;
    }
  ]
}
