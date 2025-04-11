interface RoomCardProps {
  id?: string;
  name: string;
  capacity: number;
  onClick: () => void;
}

export const RoomCard = ({ name, capacity, onClick }: RoomCardProps) => {
  return (
    <div className="bg-transparent rounded-lg shadow-md overflow-hidden border-2 border-gray-300 hover:shadow-lg transition-shadow">
      <div className="p-3">
        <h3 className="text-xl font-semibold text-gray-800">{name}</h3>
        <p className="mt-2 text-gray-600">Capacidade: {capacity} pessoas</p>
        <button
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          onClick={onClick}
        >
          Reservar
        </button>
      </div>
    </div>
  );
};
