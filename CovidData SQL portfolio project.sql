--This data is from 1st jan 2020 to 1st of Dec 2021 (23 Months)
--looking all the data

select * from PortfolioProject..CovidDeaths
order by date 


-- looking for total cases vs population
-- what percentage of population are affected

select location, date, total_cases, population, (total_cases/population)*100 as AffectedPopulation 
from PortfolioProject..CovidDeaths
order by AffectedPopulation desc


-- looking at total cases vs total deaths
-- looking for death percentage

select location,date, total_cases, total_deaths,(total_deaths/total_cases)*100 as DeathPercentage
from PortfolioProject..CovidDeaths
order by date desc

-- looking how many people got infected in the country

select location,population, max(total_cases)as HighestInfectedCount , max((total_cases/population))*100 as TotalInfectedPopulation 
from PortfolioProject..CovidDeaths
group by location,population
order by TotalInfectedPopulation desc

--looking which country has highest deaths 

select location, max(cast(total_deaths as bigint))as TotalDeathCount 
from PortfolioProject..CovidDeaths
where continent is not null
group by location
order by TotalDeathCount desc

--looking which continent has highest deaths

select continent, max(cast(total_deaths as bigint))as TotalDeathCount 
from PortfolioProject..CovidDeaths
where continent is not null
group by continent
order by TotalDeathCount desc

--- now lets see the overall cases and death count in the world

select  sum(new_cases) as total_cases, sum(cast(new_deaths as bigint)) as total_deaths, 
sum(cast(new_deaths as bigint)) / sum(new_cases)*100 as Deathpercentage
from PortfolioProject..CovidDeaths
where continent is not null
order by 1,2


-- now lets see the total population vs total vaccinations

select dea.continent,dea.location, dea.population, vac.new_vaccinations,
sum(convert(int,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date)
as RollingpeopleVaccinated
--,(RollingPeopleVaccinated/population)*100

from PortfolioProject..CovidDeaths dea 
join PortfolioProject..CovidVaccination vac
on dea.location=vac.location
and dea.date=vac.date
where dea.continent is not null
order by 2,3

-- USE CTE

with PopVsVac(Continent,Location,date,Population,new_vaccinations,RollingPeopleVaccinated)
as
(
select dea.continent,dea.location,dea.date, dea.population, vac.new_vaccinations,
sum(convert(bigint,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date)
as RollingpeopleVaccinated
--,(RollingPeopleVaccinated/population)*100

from PortfolioProject..CovidDeaths dea 
join PortfolioProject..CovidVaccination vac
on dea.location=vac.location
and dea.date=vac.date
where dea.continent is not null
)
select *, (RollingPeopleVaccinated/Population)*100 as PercentageOfPeopleVaccinated from PopVsVac


-- Temp Table

create table #PercentPeopleVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric, 
new_vaccination numeric,
RollingPeopleVaccinated numeric)

insert into #PercentPeopleVaccinated
select dea.continent,dea.location,dea.date, dea.population, vac.new_vaccinations,
sum(convert(bigint,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date)
as RollingpeopleVaccinated
--,(RollingPeopleVaccinated/population)*100

from PortfolioProject..CovidDeaths dea 
join PortfolioProject..CovidVaccination vac
on dea.location=vac.location
and dea.date=vac.date
where dea.continent is not null

select *, (RollingPeopleVaccinated/Population)*100 as PercentageOfPeopleVaccinated from #PercentPeopleVaccinated

-- create view to store data for visulization


create view PercentPopulationVaccinated as
select dea.continent,dea.location,dea.date, dea.population, vac.new_vaccinations,
sum(convert(bigint,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date)
as RollingpeopleVaccinated
--,(RollingPeopleVaccinated/population)*100

from PortfolioProject..CovidDeaths dea 
join PortfolioProject..CovidVaccination vac
on dea.location=vac.location
and dea.date=vac.date
where dea.continent is not null

select * from PercentPopulationVaccinated
