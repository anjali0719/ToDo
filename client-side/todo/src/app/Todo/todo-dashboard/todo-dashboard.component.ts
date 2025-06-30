import { Component, OnInit } from '@angular/core';
import { ToDoService } from '../ToDo.service';
import { TuiSearch } from '@taiga-ui/layout';
import { 
  TuiButton, 
  TuiTextfield 
} from '@taiga-ui/core';
import { 
  FormControl, 
  FormGroup, 
  ReactiveFormsModule 
} from '@angular/forms';
import { 
  GetTodoResponseType, 
  ToDo 
} from '../ToDo.model';

@Component({
  selector: 'app-todo-dashboard',
  imports: [
    TuiSearch,
    TuiTextfield,
    ReactiveFormsModule,
    TuiButton
  ],
  templateUrl: './todo-dashboard.component.html',
  styleUrl: './todo-dashboard.component.less'
})
export class TodoDashboardComponent implements OnInit {
  todos: ToDo[] = [
    { id: 1, title: "Renew driver's license", description: "Go for DL nenewal" },
    { id: 2, title: "Consult accountant" },
    // ...other todos
  ];

  constructor(public todoService: ToDoService) { };

  protected readonly searchForm = new FormGroup({
    search: new FormControl(),
  });


  addUpdateTodoForm = new FormGroup({
    title: new FormControl(''),
    description: new FormControl(''),
    addToFav: new FormControl(false),
    scheduleFor: new FormControl(Date)
  })

  ngOnInit(): void {
    this.todoService.toDoList().subscribe({
      next: (response: GetTodoResponseType) => {
        // debugger
        this.todos = response.items;
      },
      error: error => console.log(`Error in get-todo: ${error}`)
    });
  }

  selectedToDo: ToDo | null = null;
  isAddingNew: boolean = false;
  deleteSuccessMsg: string = '';

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

  deleteTask(toDoId: number){
    this.todoService.deleteToDo(toDoId).subscribe({
      next: (response: {status: number, message: string}) => {
        this.deleteSuccessMsg = response.message
      },
      error: err => console.log(`Error while deleting Task: ${err}`)
    });
  };

}
