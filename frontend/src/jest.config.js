/** @type {import('jest').Config} */
module.exports = {
  testEnvironment: "node", // veya "jsdom" (tarayıcı ortamı için)
  verbose: true,           // test detaylarını konsola yazdırır
  // test dosyaları için pattern
  testMatch: ["**/__tests__/**/*.test.js"], 
  // diğer ayarlar buraya eklenebilir
};
