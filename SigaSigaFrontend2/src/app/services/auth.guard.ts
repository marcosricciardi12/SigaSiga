import { Router } from '@angular/router';
import { AuthService } from './auth.service';
import { inject } from '@angular/core';

export function authGuardFactory(injectauthService: AuthService) {
  const router: Router = inject(Router);
  const is_authenticated: boolean = inject(AuthService).isAuthenticated();
    if (!is_authenticated) {
      console.log("hace algo(no autenticado)")
      router.navigate(['/home']); // Redirige al home si el usuario no está autenticado
      return false;
    }
    console.log("hace algo(autenticado)")
    return true;
}
