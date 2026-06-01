import { Routes } from '@angular/router';
import { DashboardComponent } from './views/dashboard/dashboard.component';
import { InicioComponent } from './views/inicio/inicio.component';
import { LoginComponent } from './views/login/login.component';
import { RegistroComponent } from './views/registro/registro.component';
import { QuienesSomosComponent } from './views/quienes-somos/quienes-somos.component';

export const routes: Routes = [
    { path: 'inicio', component: InicioComponent },
    { path: 'dashboard', component: DashboardComponent },
    { path: '', redirectTo: '/inicio', pathMatch: 'full' },
    { path: 'login', component: LoginComponent },
    { path: 'registro', component: RegistroComponent },
    { path: '', redirectTo: '/inicio', pathMatch: 'full' },
    { path: 'quienes-somos', component: QuienesSomosComponent },
];
