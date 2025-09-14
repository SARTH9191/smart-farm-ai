import SoilForm from "./components/SoilForm";
import SoilList from "./components/SoilList";

export default function App() {
  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">🌱 Soil Agent Dashboard</h1>
      <SoilForm onSuccess={() => window.location.reload()} />
      <SoilList />
    </div>
  );
}
