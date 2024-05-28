import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: 'tabs',
    component: TabsPage,
    children: [
      {
        path: 'transmit',
        loadChildren: () => import('../transmit/transmit.module').then( m => m.TransmitPageModule)
      },
      {
        path: 'edit',
        loadChildren: () => import('../edit/edit.module').then( m => m.EditPageModule)
      },
      {
        path: 'statistics',
        loadChildren: () => import('../statistics/statistics.module').then( m => m.StatisticsPageModule)
      },
      {
        path: 'settings',
        loadChildren: () => import('../settings/settings.module').then( m => m.SettingsPageModule)
      },
      {
        path: 'info',
        loadChildren: () => import('../info/info.module').then( m => m.InfoPageModule)
      },
      {
        path: '',
        redirectTo: '/tabs/info',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: '',
    redirectTo: '/tabs/info',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
})
export class TabsPageRoutingModule {}
