export type Status = 'to-start' | 'in-progress' | 'completed';
export type Priority = 'high' | 'medium' | 'low';

export interface ToDo {
  id: number;
  title: string;
  description?: string;
  dueDate?: Date;
  priority?: Priority;
  completed?: boolean;
  status?: Status;
}

// Todo return is most prolly the whole todo object from db

// id
// title= req.title,
// description= req.description,
// add_to_favourites= req.add_to_favourites,
// completed= req.completed,
// scheduled_for= req.scheduled_for,
// user_id= user.get('user_id')


export interface GetTodoResponseType {
  // items: ToDo[]
  items: [],
  limit: number,
  offset: number,
  total: number,
}
