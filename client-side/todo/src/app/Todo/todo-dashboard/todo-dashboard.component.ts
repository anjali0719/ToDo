import { Component, OnInit } from '@angular/core';
import { GetTodoResponseType, ToDo } from '../ToDo.model';
import { ToDoService } from '../ToDo.service';
import { TuiSearch } from '@taiga-ui/layout';
import { TuiButton, TuiTextfield } from '@taiga-ui/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';

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
    { id: 2, title: "Consult accountant"},
    // ...other todos
  ];

  constructor(public todoService: ToDoService){};

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
    this.todoService.getToDo().subscribe({
      next: (response: GetTodoResponseType) => {
        // debugger
        this.todos = response.items;
      },
      error: error => console.log(`Error in get-todo: ${error}`)
    });
  }

  selectedToDo: ToDo | null = null;
  isAddingNew: boolean = false;

  selectToDo(todo: ToDo){
    this.selectedToDo = todo;
    this.isAddingNew = false;
  };

  closeEditPanel(){
    this.selectedToDo = null;
    this.isAddingNew = false;
  };

  openAddNewTask(){
    this.isAddingNew = true;
  };

}
