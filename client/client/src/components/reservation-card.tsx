interface ReservationCardProps {
  reservation: {
    id: string;
    room_id: string;
    date: string;
    start_time: string;
    end_time: string;
    status: string;
    room?: {
      // Opcional caso venha junto
      name: string;
      capacity: number;
    };
  };
  onCancel: (id: string) => void;
}

export function ReservationCard({
  reservation,
  onCancel,
}: ReservationCardProps) {
  // Formata a data para o formato brasileiro
  const formatDate = (dateString: string) => {
    const [year, month, day] = dateString.split("-");
    return `${day}/${month}/${year}`;
  };

  // Combina data e hora para exibição
  const formatTimeRange = () => {
    return `${formatDate(reservation.date)} - ${reservation.start_time.slice(
      0,
      5
    )} às ${reservation.end_time.slice(0, 5)}`;
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-medium text-lg">
            {reservation.room?.name ||
              `Sala ${reservation.room_id.slice(0, 4)}`}
          </h3>

          {reservation.room?.capacity && (
            <p className="text-gray-600">
              Capacidade: {reservation.room.capacity}
            </p>
          )}

          <div className="mt-2 space-y-1">
            <p className="text-sm">
              <span className="font-medium">Data/Horário:</span>{" "}
              {formatTimeRange()}
            </p>
            <p className="text-sm">
              <span className="font-medium">Status:</span>{" "}
              <span
                className={`px-2 py-1 rounded text-xs ${
                  reservation.status === "confirmed"
                    ? "bg-green-100 text-green-800"
                    : reservation.status === "cancelled"
                    ? "bg-red-100 text-red-800"
                    : "bg-yellow-100 text-yellow-800"
                }`}
              >
                {reservation.status === "confirmed"
                  ? "Confirmada"
                  : reservation.status === "cancelled"
                  ? "Cancelada"
                  : "Pendente"}
              </span>
            </p>
          </div>
        </div>

        {reservation.status !== "cancelled" && (
          <button
            onClick={() => onCancel(reservation.id)}
            className="bg-red-600 text-white px-3 py-1 rounded text-sm shadow-lg hover:bg-red-700 transition-colors"
            title="Cancelar reserva"
          >
            Cancelar
          </button>
        )}
      </div>
    </div>
  );
}
