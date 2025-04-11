import { useEffect, useState } from "react";
import axios from "axios";

interface Room {
  id: number;
  name: string;
  capacity: number;
}

export default function RoomList() {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const response = await axios.get("http://localhost:8000/rooms");
        setRooms(response.data);
      } catch (error) {
        console.error("Error fetching rooms:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchRooms();
  }, []);

  if (loading)
    return <div className="text-center py-8">Carregando salas...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Salas Disponíveis</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {rooms.map((room) => (
          <div key={room.id} className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold">{room.name}</h2>
            <p className="text-gray-600 mt-2">
              Capacidade: {room.capacity} pessoas
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
