import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { TransmitPageRoutingModule } from './transmit-routing.module';

import { TransmitPage } from './transmit.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    TransmitPageRoutingModule
  ],
  declarations: [TransmitPage]
})
export class TransmitPageModule {}
