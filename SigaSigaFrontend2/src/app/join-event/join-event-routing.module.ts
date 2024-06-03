import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { JoinEventPage } from './join-event.page';

const routes: Routes = [
  {
    path: '',
    component: JoinEventPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class JoinEventPageRoutingModule {}
