import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TransmitPage } from './transmit.page';

const routes: Routes = [
  {
    path: '',
    component: TransmitPage
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class TransmitPageRoutingModule {}
