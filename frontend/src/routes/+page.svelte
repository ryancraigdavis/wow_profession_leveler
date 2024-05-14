<!-- src/routes/+page.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';

  let regions = ['EU', 'NA'];
  let selectedRegion = '';
  let realms: string[] = [];
  let realmData: { [key: string]: number } = {};
  let selectedRealm = '';
  let selectedFaction = '';
  let selectedProfession = '';
  let showErrorMessage = false;
  let showRealmError = false;

  const factions = ['Alliance', 'Horde'];
  const professions = ['Alchemy', 'Blacksmithing', 'Jewelcrafting', 'Engineering', 'Leatherworking', 'Tailoring', 'Inscription'];

  async function loadRealms(region: string) {
    try {
      const response = await fetch(`/${region.toLowerCase()}_realms.json`);
      if (!response.ok) {
        throw new Error(`Failed to load ${region} realms`);
      }
      const data = await response.json();
      realmData = data;
      realms = Object.keys(data);
      selectedRealm = ''; // Reset the selected realm when region changes
    } catch (error) {
      console.error(`Error loading ${region} realms:`, error);
      showRealmError = true;
    }
  }

  function handleRegionChange() {
    if (selectedRegion) {
      loadRealms(selectedRegion);
    } else {
      realms = [];
      selectedRealm = '';
    }
  }

  function handleSubmit() {
    if (selectedRealm && selectedFaction && selectedProfession) {
      // TODO: Implement the logic to handle form submission
      console.log('Region:', selectedRegion);
      console.log('Realm:', selectedRealm);
      console.log('Realm ID:', realmData[selectedRealm]);
      console.log('Faction:', selectedFaction);
      console.log('Profession:', selectedProfession);
    } else {
      showErrorMessage = true;
    }
  }
</script>

<main>
  <h1>WoW Cataclysm Classic Profession Leveling</h1>

  {#if showErrorMessage}
    <div class="error-message">
      Please select a region, realm, faction, and profession before submitting.
    </div>
  {/if}

  <div>
    <label for="region">Region:</label>
    <select id="region" bind:value={selectedRegion} on:change={handleRegionChange}>
      <option value="">Select a region</option>
      {#each regions as region}
        <option value={region}>{region}</option>
      {/each}
    </select>
  </div>

  <div>
    <label for="realm">Realm:</label>
    <select id="realm" bind:value={selectedRealm} disabled={!selectedRegion}>
      <option value="">Select a realm</option>
      {#each realms as realm}
        <option value={realm}>{realm}</option>
      {/each}
    </select>
    {#if showRealmError}
      <div class="error-message">
        Failed to load realms. Please check the {selectedRegion.toLowerCase()}_realms.json file.
      </div>
    {/if}
  </div>

  <div>
    <label for="faction">Faction:</label>
    <select id="faction" bind:value={selectedFaction}>
      <option value="">Select a faction</option>
      {#each factions as faction}
        <option value={faction}>{faction}</option>
      {/each}
    </select>
  </div>

  <div>
    <label for="profession">Profession:</label>
    <select id="profession" bind:value={selectedProfession}>
      <option value="">Select a profession</option>
      {#each professions as profession}
        <option value={profession}>{profession}</option>
      {/each}
    </select>
  </div>

  <button on:click={handleSubmit}>Submit</button>

</main>

<style>
  .error-message {
    color: red;
    margin-bottom: 1rem;
  }
</style>
