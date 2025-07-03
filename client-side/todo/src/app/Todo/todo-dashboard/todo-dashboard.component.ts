import {
  Component,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import {
  TuiButton,
  TuiIcon,
  TuiTextfield
} from '@taiga-ui/core';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import {
  Counts,
  DateUtils,
  GetTodoResponseType,
  ToDo
} from '../ToDo.model';
import {
  TuiCheckbox,
  TuiChevron,
  TuiDataListWrapper,
  TuiInputDate,
  TuiLike,
  TuiSelect,
  TuiTextarea
} from '@taiga-ui/kit';
import { ToDoService } from '../ToDo.service';
import { TuiSearch } from '@taiga-ui/layout';
import { TuiDay } from '@taiga-ui/cdk/date-time';
import { Router } from '@angular/router';
import { Observable, switchMap } from 'rxjs';

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
    FormsModule,
    TuiLike,
    TuiCheckbox,
    TuiIcon
  ],
  templateUrl: './todo-dashboard.component.html',
  styleUrl: './todo-dashboard.component.less',
  encapsulation: ViewEncapsulation.None
})
export class TodoDashboardComponent implements OnInit {

  // Constructors
  constructor(
    public todoService: ToDoService,
    public router: Router
  ) { };

  // FormControls
  protected readonly today = TuiDay.currentLocal();
  protected readonly min = new TuiDay(this.today.year, this.today.month, 1);
  protected readonly max = this.min.append({ month: 6, day: -1 });
  protected readonly handler = (day: TuiDay): boolean => day.daySame(this.today);

  protected readonly searchForm = new FormGroup({
    search: new FormControl(),
    value: new FormControl()
  });

  addUpdateTodoForm = new FormGroup({
    title: new FormControl('', [Validators.required, Validators.minLength(3)]),
    description: new FormControl('', Validators.minLength(3)),
    addToFav: new FormControl(false),
    completed: new FormControl(false),
    dateControl: new FormControl(TuiDay.fromLocalNativeDate(new Date()))
  })

  // Oninit
  ngOnInit(): void {
    this.onTabSelection(this.selectedTab);
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
  selectedTab: string = "today";
  count: Counts = {
    today: 0,
    upcoming: 0,
    favourites: 0,
    completed: 0,
  };

  // API Calls and Other action methods
  onTabSelection(tab: string) {
    this.selectedTab = tab;
    const search = this.searchForm.value.search;
    return this.todoService.toDoList(search, tab).subscribe({
      next: (response: GetTodoResponseType) => {
        // debugger
        this.todos = response.results.items;
        this.count = response.counts;
        this.closeEditPanel();
      },
      error: (error) => {
        if (error.status === 401) {
          this.router.navigate(['/user/sign-in/'])
        } else {
          console.log(`Error in get-todo: ${JSON.stringify(error)}`)
        }
      }
    });
  };

  selectToDo(todo: ToDo) {
    const dateObj = new Date(todo.scheduled_for)
    this.isAddingNew = false;
    this.selectedToDo = todo;
    this.addUpdateTodoForm.patchValue({
      title: todo.title,
      description: todo.description,
      addToFav: todo.add_to_favourites,
      completed: todo.completed,
      dateControl: new TuiDay(dateObj.getFullYear(), dateObj.getMonth(), dateObj.getDate())
    });
  };

  closeEditPanel() {
    this.selectedToDo = null;
    this.isAddingNew = false;
  };

  openAddNewTask() {
    this.isAddingNew = true;
    this.addUpdateTodoForm.reset({
      dateControl: TuiDay.fromLocalNativeDate(new Date()),
      completed: false,
      addToFav: false
    });
  };

  createTodo() {
    const title = this.addUpdateTodoForm.value.title ?? ''
    const description = this.addUpdateTodoForm.value.description ?? ''
    const addToFav = this.addUpdateTodoForm.value.addToFav ?? false
    const completed = this.addUpdateTodoForm.value.completed ?? false
    const scheduledFor = DateUtils.combineDateWithCurrentTime(this.addUpdateTodoForm.value.dateControl!) ?? new Date().toISOString()
    this.todoService.createToDo(title, description, addToFav, completed, scheduledFor).subscribe({
      next: (response) => {
        console.log(`Success`);
        this.closeEditPanel();
        this.onTabSelection(this.selectedTab);
      },
      error: err => console.log(`Error while creating Task: ${JSON.stringify(err)}`)
    })
  };

  updateTodo() {
    const todoId = this.selectedToDo?.id!
    const title = this.addUpdateTodoForm.value.title ?? ''
    const description = this.addUpdateTodoForm.value.description ?? ''
    const addToFav = this.addUpdateTodoForm.value.addToFav ?? false
    const completed = this.addUpdateTodoForm.value.completed ?? false
    const scheduledFor = DateUtils.combineDateWithCurrentTime(this.addUpdateTodoForm.value.dateControl!) ?? new Date().toISOString()
    this.todoService.updateToDo(todoId, title, description, addToFav, completed, scheduledFor).subscribe({
      next: (response) => {
        console.log(`Success`);
        // Refresh the UI, to get the updated list
      },
      error: err => console.log(`Error while updating Task: ${JSON.stringify(err)}`)
    });
  };

  deleteTask(toDoId: number) {
    this.todoService.deleteToDo(toDoId).subscribe({
      next: (response: { status: number, message: string }) => {
        this.deleteSuccessMsg = response.message;
        this.router.navigate(['/todo/todo-dashboard/'])
      },
      error: err => console.log(`Error while deleting Task: ${JSON.stringify(err)}`)
    });
  };

  signOut(){
    localStorage.clear()
    this.router.navigate(['/user/sign-in/'])
  };

}
