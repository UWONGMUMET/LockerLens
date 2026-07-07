import EmptyHistoryState from './EmptyHistoryState.jsx';
import HistoryListItem from './HistoryListItem.jsx';

export default function HistoryList({ items, selectedId, onSelect, onDelete, deletingId }) {
  if (items.length === 0) return <EmptyHistoryState compact />;

  return (
    <div className="grid gap-3">
      {items.map((item) => (
        <HistoryListItem
          key={item.id}
          item={item}
          selected={selectedId === item.id}
          onSelect={onSelect}
          onDelete={onDelete}
          deleting={deletingId === item.id}
        />
      ))}
    </div>
  );
}
