import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DirectorPage } from './director.page';

const routes: Routes = [
  {
    path: '',
    component: DirectorPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class DirectorPageRoutingModule {}
