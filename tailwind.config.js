/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [
    require("tailwindcss/plugin")(({ addVariant }) => {
      addVariant("child", "&>*");
    }),
  ],
};
