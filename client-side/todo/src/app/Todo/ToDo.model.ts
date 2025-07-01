export type Status = 'to-start' | 'in-progress' | 'completed';
export type Priority = 'high' | 'medium' | 'low';

export interface ToDo {
  id: number | null;
  title: string;
  description?: string;
  dueDate?: Date;
  priority?: Priority;
  completed?: boolean;
  status?: Status;
}

// Todo return is most prolly the whole todo object from db

// {
//     "title": "wyitime",
//     "description": "This tdod will test the time",
//     "add_to_favourites": false,
//     "id": 21,
//     "user_id": 7,
//     "notification_sent_at": null,
//     "auto_updated": false,
//     "completed": false,
//     "created_at": "2025-06-30T13:35:55.149463+00:00",
//     "updated_at": null,
//     "scheduled_for": "2025-07-15T13:45:54.655000+00:00"
// }


export interface GetTodoResponseType {
  // items: ToDo[]
  items: [],
  limit: number,
  offset: number,
  total: number,
}
