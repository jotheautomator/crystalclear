import { Routes, Route } from "react-router-dom";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        <Route
          path="/"
          element={
            <div className="flex items-center justify-center min-h-screen">
              <div className="text-center">
                <h1 className="text-4xl font-bold text-crystal-700">
                  CrystalClear
                </h1>
                <p className="mt-2 text-gray-500">
                  Political Transparency Platform
                </p>
              </div>
            </div>
          }
        />
      </Routes>
    </div>
  );
}
