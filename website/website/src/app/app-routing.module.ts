import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { MainComponent } from './main/main.component';
import { ResultSearchComponent } from "./result-search/result-search.component";
import { AboutUsComponent } from "./about-us/about-us.component";
import { NotFoundComponent } from "./not-found/not-found.component";

const appRoutes: Routes = [
  {
    path: '',
    component: MainComponent,
    pathMatch: 'full'
  },
  {
    path: 'result/:what',
    component: ResultSearchComponent
  },
  {
    path: 'about',
    component: AboutUsComponent
  },
  {
    path: '**', component: NotFoundComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(
      appRoutes
    )
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule { }
