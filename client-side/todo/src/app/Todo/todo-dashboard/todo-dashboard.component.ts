import {
  Component,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import {
  TuiButton,
  TuiTextfield
} from '@taiga-ui/core';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule
} from '@angular/forms';
import {
  GetTodoResponseType,
  ToDo
} from '../ToDo.model';
import {
  TuiChevron,
  TuiDataListWrapper,
  TuiInputDate,
  TuiSelect,
  TuiTextarea
} from '@taiga-ui/kit';
import { ToDoService } from '../ToDo.service';
import { TuiSearch } from '@taiga-ui/layout';
import { TuiDay } from '@taiga-ui/cdk/date-time';

@Component({
  selector: 'app-todo-dashboard',
  imports: [
    TuiSearch,
    TuiTextfield,
    ReactiveFormsModule,
    TuiButton,
    TuiInputDate,
    TuiTextarea,
    TuiChevron,
    TuiDataListWrapper,
    TuiSelect,
    FormsModule
  ],
  templateUrl: './todo-dashboard.component.html',
  styleUrl: './todo-dashboard.component.less',
  encapsulation: ViewEncapsulation.None
})
export class TodoDashboardComponent implements OnInit {

  // Constructors
  constructor(public todoService: ToDoService) { };

  // FormControls
  dateControl = new FormControl(new TuiDay(2025, 6, 30));

  protected readonly searchForm = new FormGroup({
    search: new FormControl(),
    value: new FormControl()
  });

  addUpdateTodoForm = new FormGroup({
    title: new FormControl(''),
    description: new FormControl(''),
    addToFav: new FormControl(false),
    scheduleFor: new FormControl(Date)
  })

  // Oninit
  ngOnInit(): void {
    this.todoService.toDoList().subscribe({
      next: (response: GetTodoResponseType) => {
        // debugger
        this.todos = response.items;
      },
      error: error => console.log(`Error in get-todo: ${error}`)
    });
  };

  // Define Variables
  protected readonly listOptions = [
    'Personal',
    'Work',
    'List 1'
  ];
  todos: ToDo[] = [];
  selectedToDo: ToDo | null = null;
  isAddingNew: boolean = false;
  deleteSuccessMsg: string = '';

  // API Calls and Other action methods
  selectToDo(todo: ToDo) {
    this.selectedToDo = todo;
    this.addUpdateTodoForm.get('title')?.patchValue(todo.title ?? '');
    this.addUpdateTodoForm.get('description')?.patchValue(todo.description ?? '');
    this.isAddingNew = false;
  };

  closeEditPanel() {
    this.selectedToDo = null;
    this.isAddingNew = false;
  };

  openAddNewTask() {
    this.selectedToDo = {
      id: null,
      title: '',
      description: '',
    };
    this.isAddingNew = true;
    this.addUpdateTodoForm.reset();
  };

  deleteTask(toDoId: number) {
    this.todoService.deleteToDo(toDoId).subscribe({
      next: (response: { status: number, message: string }) => {
        this.deleteSuccessMsg = response.message
      },
      error: err => console.log(`Error while deleting Task: ${err}`)
    });
  };

}
