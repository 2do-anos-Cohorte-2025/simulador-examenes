import { Component } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './views/dashboard/dashboard.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    RouterLink,
    CommonModule,
    DashboardComponent
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  title = 'proyecto';

  arrowUrl: string = 'assets/icons/arrow-up.svg';
  checkUrl: string = 'assets/icons/checkbox.svg';

  constructor(private router: Router) {}

  isHomeRoute(): boolean {
    return this.router.url === '/';
  }
}
