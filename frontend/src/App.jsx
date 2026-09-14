import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import MachineList from "./pages/MachineList";
import RotaProtegida from "./components/RotaProtegida";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route
          path="/maquinas"
          element={
            <RotaProtegida>
              <MachineList />
            </RotaProtegida>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
