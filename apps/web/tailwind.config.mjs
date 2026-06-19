const config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#172126",
        panel: "#f7f4ec",
        line: "#d8d2c3",
        moss: "#466b4f",
        clay: "#b45f43",
        sea: "#2e6f83",
        plum: "#6d5773",
      },
      boxShadow: {
        surface: "0 18px 45px rgba(23, 33, 38, 0.08)",
      },
    },
  },
  plugins: [],
};

export default config;