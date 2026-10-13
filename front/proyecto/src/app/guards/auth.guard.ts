import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../service/AuthService/auth.service';

// Solo usuarios logueados
export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  return auth.estaLogueado() ? true : router.createUrlTree(['/login']);
};
