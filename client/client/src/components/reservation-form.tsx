import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { base_url } from "../context/auth-context";

interface Room {
  id: string;
  name: string;
}

interface ReservationFormData {
  room_id: string;
  date: string;
  start_time: string;
  end_time: string;
  status: string;
}

export default function CreateReservationForm({
  rooms,
  user_id,
  onClose,
}: {
  rooms: Room[];
  user_id: string;
  onClose: () => void;
}) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<ReservationFormData>({
    room_id: "",
    date: "",
    start_time: "09:00",
    end_time: "10:00",
    status: "pending",
  });
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError("");

    try {
      const payload = {
        ...formData,
        start_time: `${formData.start_time}:00`,
        end_time: `${formData.end_time}:00`,
        user_id: user_id, //"7e1dcd34-5a67-48d6-8866-e78ea3d2f5e1",
      };

      const response = await axios.post(base_url + "/reservations", payload);

      if (response.status === 201) {
        navigate("/dashboard", {
          state: {
            success: `Reserva criada com sucesso! ID: ${response.data.reservation_id}`,
          },
        });
      }
      onClose();
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.message || "Erro ao criar reserva");
      } else {
        setError("Ocorreu um erro inesperado");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const isTimeValid = () => {
    if (!formData.start_time || !formData.end_time) return true;
    return formData.end_time > formData.start_time;
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md w-full">
      <div className="flex flex-row justify-between items-center mb-6 px-1 pb-4">
        <h2 className="text-2xl font-bold text-center">Nova Reserva</h2>
        <button onClick={onClose} className="text-gray-500">
          X
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">{error}</div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 mb-2" htmlFor="room_id">
            Sala *
          </label>
          <select
            id="room_id"
            name="room_id"
            value={formData.room_id}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded"
            required
          >
            <option value="">Selecione uma sala</option>
            {rooms.map((room) => (
              <option key={room.id} value={room.id}>
                {room.name}
              </option>
            ))}
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-gray-700 mb-2" htmlFor="date">
            Data *
          </label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded"
            min={new Date().toISOString().split("T")[0]}
            required
          />
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-gray-700 mb-2" htmlFor="start_time">
              Hora Início *
            </label>
            <input
              type="time"
              id="start_time"
              name="start_time"
              value={formData.start_time}
              onChange={handleChange}
              className="w-full px-3 py-2 border rounded"
              min="08:00"
              max="18:00"
              required
            />
          </div>

          <div>
            <label className="block text-gray-700 mb-2" htmlFor="end_time">
              Hora Fim *
            </label>
            <input
              type="time"
              id="end_time"
              name="end_time"
              value={formData.end_time}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded ${
                !isTimeValid() ? "border-red-500" : ""
              }`}
              min="08:00"
              max="18:00"
              required
            />
            {!isTimeValid() && (
              <p className="text-red-500 text-xs mt-1">
                O horário final deve ser após o inicial
              </p>
            )}
          </div>
        </div>

        <div className="mb-6">
          <label className="block text-gray-700 mb-2" htmlFor="status">
            Status
          </label>
          <select
            id="status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded"
          >
            <option value="pending">Pendente</option>
            <option value="confirmed">Confirmada</option>
          </select>
        </div>

        <button
          type="submit"
          disabled={isSubmitting || !isTimeValid()}
          className={`w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition-colors ${
            isSubmitting || !isTimeValid()
              ? "opacity-50 cursor-not-allowed"
              : ""
          }`}
        >
          {isSubmitting ? "Criando Reserva..." : "Criar Reserva"}
        </button>
      </form>
    </div>
  );
}
