import { Routes } from '@angular/router';

import { QuienesSomosComponent } from './views/quienes-somos/quienes-somos.component';
import { ProfesionalComponent } from './views/profesional/profesional.component';

export const routes: Routes = [
  {
    path: 'quienes-somos',
    component: QuienesSomosComponent
  },
  {
    path: 'quienes-somos/:id',
    component: ProfesionalComponent
  }
];
