import axios from "axios";
import { useEffect, useState } from "react";
import { base_url, useAuth } from "../context/auth-context";
import { ReservationCard } from "./reservation-card";
import CreateReservationForm from "./reservation-form";
import { RoomCard } from "./room-card";

export interface Room {
  id: string;
  name: string;
  capacity: number;
}

export interface Reservation {
  id: string;
  room_id: string;
  date: string;
  start_time: string;
  end_time: string;
  status: string;
}

export default function Dashboard() {
  const { logout } = useAuth();
  const [rooms, setRooms] = useState<Room[]>([]);
  const [myReservations, setMyReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState({
    rooms: true,
    reservations: true,
  });
  const [showReservationForm, setShowReservationForm] = useState(false);
  const user_info = JSON.parse(localStorage.getItem("user") || "");

  const fetchRoom = async () => {
    try {
      const response = await axios.get<{ room: Room[] }>(base_url + "/rooms");
      setRooms(response.data.room);
      setLoading((prev) => ({ ...prev, rooms: false }));
    } catch (err) {
      console.error("Error fetching rooms:", err);
      setLoading((prev) => ({ ...prev, rooms: false }));
    }
  };

  const fetchReservation = async () => {
    try {
      const response = await axios.get<{
        reservations: any;
      }>(
        base_url + `/reservations/user/${user_info.id}` //7e1dcd34-5a67-48d6-8866-e78ea3d2f5e1
      );
      setMyReservations(response.data.reservations);
      setLoading((prev) => ({ ...prev, reservations: false }));
    } catch (err) {
      console.error("Error fetching reservations:", err);
      setLoading((prev) => ({ ...prev, reservations: false }));
    }
  };

  useEffect(() => {
    /*const fetchData = async () => {
      try {
        const response = await axios.get<{ room: Room[] }>(base_url + "/rooms");
        setRooms(response.data.room);
        setLoading((prev) => ({ ...prev, rooms: false }));
      } catch (err) {
        console.error("Error fetching rooms:", err);
        setLoading((prev) => ({ ...prev, rooms: false }));
      }

      try {
        const response = await axios.get<{
          reservations: any;
        }>(
          base_url + `/reservations/user/${user_info.id}` //7e1dcd34-5a67-48d6-8866-e78ea3d2f5e1
        );
        setMyReservations(response.data.reservations);
        setLoading((prev) => ({ ...prev, reservations: false }));
      } catch (err) {
        console.error("Error fetching reservations:", err);
        setLoading((prev) => ({ ...prev, reservations: false }));
      }
    };*/

    fetchRoom();
    fetchReservation();
  }, []);

  console.log(rooms);

  useEffect(() => {
    const roomSocket = new WebSocket(base_url + "/ws/rooms");

    roomSocket.onopen = () => {
      console.log("Conectado ao WebSocket");
    };

    roomSocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === "new_room") {
        console.log(message);
        const novaSala: Room = message.data;
        setRooms((prev) => [...prev, novaSala]);
      }
    };

    roomSocket.onerror = (err) => {
      console.error("Erro no WebSocket:", err);
    };

    roomSocket.onclose = () => {
      console.log("WebSocket desconectado");
    };

    return () => {
      roomSocket.close();
    };
  }, []);

  const handleCancelReservation = async (reservationId: string) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/reservations/${reservationId}`);
      setMyReservations((prev) =>
        prev.filter((reservation) => reservation.id !== reservationId)
      );
    } catch (err) {
      console.error("Error canceling reservation:", err);
      alert("Falha ao cancelar reserva");
    }
  };

  const onOpenReservationModal = () => {
    setShowReservationForm(true);
  };

  const onCloseReservationModal = () => {
    setShowReservationForm(false);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <button
            onClick={logout}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Sair
          </button>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg min-h-96">
            {loading.rooms ? (
              <p className="text-center mt-40 text-gray-500">
                Carregando Salas...
              </p>
            ) : rooms.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
                {rooms.map((room) => (
                  <RoomCard
                    key={room.id}
                    id={room.id}
                    name={room.name}
                    capacity={room.capacity}
                    onClick={onOpenReservationModal}
                  />
                ))}
              </div>
            ) : (
              <p className="text-center mt-40 text-gray-500">
                Nenhuma sala disponível no momento
              </p>
            )}
          </div>
        </div>
        <div className="px-4 py-6 sm:px-0">
          <h2 className="text-start text-2xl text-gray-700">Minhas Reservas</h2>
          <div className="p-6">
            {loading.reservations ? (
              <div className="flex justify-center items-center h-40">
                <p className="text-gray-500 animate-pulse">
                  Carregando reservas...
                </p>
              </div>
            ) : myReservations.length > 0 ? (
              <div className="space-y-4">
                {myReservations.map((reservation) => {
                  const roomDetails = rooms.find(
                    (r) => r.id === reservation.room_id
                  );

                  return (
                    <ReservationCard
                      key={reservation.id}
                      reservation={{
                        ...reservation,
                        room: roomDetails,
                      }}
                      onCancel={handleCancelReservation}
                    />
                  );
                })}
              </div>
            ) : (
              <div className="flex justify-center items-center h-40">
                <p className="text-gray-500">Você não possui reservas</p>
              </div>
            )}
          </div>
        </div>
      </main>

      {showReservationForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <CreateReservationForm
            rooms={rooms}
            user_id={user_info.id}
            onClose={onCloseReservationModal}
          />
        </div>
      )}
    </div>
  );
}
