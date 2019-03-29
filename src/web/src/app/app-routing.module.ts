import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ResultsComponent } from './results/results.component';
import { AboutUsComponent } from './about-us/about-us.component';

const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'results', component: ResultsComponent },
    { path: 'about-us', component: AboutUsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
