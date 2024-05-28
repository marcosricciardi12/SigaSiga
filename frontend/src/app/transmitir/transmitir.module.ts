import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { TransmitirPageRoutingModule } from './transmitir-routing.module';

import { TransmitirPage } from './transmitir.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    TransmitirPageRoutingModule
  ],
  declarations: [TransmitirPage]
})
export class TransmitirPageModule {}
