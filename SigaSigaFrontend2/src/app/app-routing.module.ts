import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
// import { authGuardFactory } from './services/auth.guard';
import { authGuardFactory } from './services/auth.guard';

const routes: Routes = [
  {
    path: 'menu',
    loadChildren: () => import('./tabs/tabs.module').then(m => m.TabsPageModule),
    canActivate: [authGuardFactory]
  },
  {
    path: 'transmit',
    loadChildren: () => import('./transmit/transmit.module').then( m => m.TransmitPageModule),
    canActivate: [authGuardFactory]
  },
  {
    path: 'edit',
    loadChildren: () => import('./edit/edit.module').then( m => m.EditPageModule),
    canActivate: [authGuardFactory]
  },
  {
    path: 'statistics',
    loadChildren: () => import('./statistics/statistics.module').then( m => m.StatisticsPageModule),
    canActivate: [authGuardFactory]
  },
  {
    path: 'settings',
    loadChildren: () => import('./settings/settings.module').then( m => m.SettingsPageModule),
    canActivate: [authGuardFactory]
  },
  {
    path: 'info',
    loadChildren: () => import('./info/info.module').then( m => m.InfoPageModule),
    canActivate: [authGuardFactory]
  },
  {
    path: 'home',
    loadChildren: () => import('./home/home.module').then( m => m.HomePageModule)
  },
  {
    path: '',
    loadChildren: () => import('./home/home.module').then( m => m.HomePageModule)
  },
  {
    path: 'director',
    loadChildren: () => import('./director/director.module').then( m => m.DirectorPageModule)
  },
  {
    path: 'join-event',
    loadChildren: () => import('./join-event/join-event.module').then( m => m.JoinEventPageModule)
  }
];
@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {}
