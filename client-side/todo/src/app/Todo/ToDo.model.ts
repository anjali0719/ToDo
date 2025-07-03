import { TuiDay } from "@taiga-ui/cdk/date-time";

// todo object after create & update

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

// todo object in get-todo-list response
export interface ToDo {
  id: number | null;
  title: string;
  description: string;
  completed: boolean;
  add_to_favourites: boolean;
  scheduled_for: string;
}

// response type of get-todo-list
export interface GetTodoResponseType {
  counts: Counts,
  results: ToDoListResults
}

export interface Counts {
  today: number,
  upcoming: number,
  favourites: number,
  completed: number,
  [key: string]: number
}

export interface ToDoListResults {
  items: ToDo[],
  limit: number,
  offset: number,
  total: number
}


// move this to separate file
export class DateUtils {
  static combineDateWithCurrentTime(tuiDay: TuiDay): string {
    const now = new Date();

    // Build ISO string directly without creating local Date object
    const year = tuiDay.year;
    const month = String(tuiDay.month + 1).padStart(2, '0');
    const day = String(tuiDay.day).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const ms = String(now.getMilliseconds()).padStart(3, '0');

    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}.${ms}Z`;
  };
};
