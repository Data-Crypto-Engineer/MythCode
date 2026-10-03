/**
 * MythCode — Adaptive Multi-Agent Fantasy Adventure & Experiential Programming Learning Platform
 *
 * Central Design Principle:
 * "The player should discover computational thinking because they are trying to solve
 * a problem in the fantasy world. They should not feel like they have opened a programming course."
 *
 * Language-Neutral Computational Layer:
 * - ACTION (Sequence)
 * - CONDITION (Branching / If-Else)
 * - REPETITION (Loops / Iteration)
 * - VALUE (Variables / Named Data)
 * - REUSABLE_ACTION (Functions / Abstraction)
 * - COLLECTION (Lists / Dictionaries / Data Structures)
 *
 * Learning Journal:
 * - The Codex of Becoming: Discoveries, Masteries, Your Craft
 */

import React, { useState } from 'react';
import {
  Sparkles,
  BookOpen,
  Compass,
  Cpu,
  RotateCcw,
  CheckCircle2,
  AlertCircle,
  Code2,
  Terminal,
  User,
  ArrowRight,
  Flame,
  Droplets,
  HelpCircle,
  Play,
  Layers,
  Award,
  Zap,
  Shield,
  Key,
  Database,
  Sliders,
  ChevronRight,
  Check,
  RefreshCw,
  Eye,
  Info
} from 'lucide-react';

// Language-Neutral Computational Primitive Types
export type ComputationalPrimitive =
  | 'ACTION'
  | 'CONDITION'
  | 'REPETITION'
  | 'VALUE'
  | 'REUSABLE_ACTION'
  | 'COLLECTION';

export interface EpiphanyReveal {
  primitive: ComputationalPrimitive;
  fantasyProblem: string;
  fantasySolution: string;
  programmingConcept: string;
  explanation: string;
  pythonSyntax: string;
  javascriptSyntax: string;
}

export interface PlayerProfile {
  name: string;
  role: string;
  style: string;
  challengeLevel: number;
  traits: {
    exploration: number;
    dialogue: number;
    puzzle: number;
    building: number;
  };
  conceptMastery: {
    sequence: number;     // Level 1
    conditions: number;   // Level 2
    loops: number;        // Level 3
    variables: number;    // Level 4
    functions: number;    // Level 5
    collections: number;  // Level 6
  };
}

export interface WorldState {
  kingdom: string;
  location: string;
  waterSupply: 'damaged' | 'investigating' | 'restoring' | 'restored';
  spiritTrust: number;
  guardianStatus: 'inactive' | 'operational';
  lunarObsStatus: 'locked' | 'aligned';
  workshopStatus: 'dormant' | 'ignited';
  archiveStatus: 'sealed' | 'opened';
  villageMorale: number;
  unresolvedConflicts: string[];
}

export interface AgentTelemetry {
  agent: string;
  role: string;
  output: string;
  status: 'approved' | 'executed' | 'verified';
}

export interface DiscoveryItem {
  id: string;
  title: string;
  location: string;
  lore: string;
  dateUnlocked: string;
}

export interface ScribedSpell {
  name: string;
  primitive: ComputationalPrimitive;
  fantasyIncantation: string;
  universalLogic: string;
  pythonEquivalent: string;
  jsEquivalent: string;
}

// -------------------------------------------------------------
// MAIN COMPONENT
// -------------------------------------------------------------
export default function App() {
  // Navigation
  const [activeTab, setActiveTab] = useState<'adventure' | 'challenges' | 'codex' | 'world' | 'agents'>('adventure');
  const [gameStarted, setGameStarted] = useState<boolean>(true);
  const [selectedLanguageSyntax, setSelectedLanguageSyntax] = useState<'python' | 'javascript'>('python');

  // Character State
  const [player, setPlayer] = useState<PlayerProfile>({
    name: 'Aria',
    role: 'Aether Scholar',
    style: 'Inquisitive & Methodical',
    challengeLevel: 1,
    traits: { exploration: 0.6, dialogue: 0.5, puzzle: 0.7, building: 0.4 },
    conceptMastery: {
      sequence: 0,
      conditions: 0,
      loops: 0,
      variables: 0,
      functions: 0,
      collections: 0
    }
  });

  // World State
  const [world, setWorld] = useState<WorldState>({
    kingdom: 'Elarion',
    location: 'Whispering Village',
    waterSupply: 'damaged',
    spiritTrust: 0,
    guardianStatus: 'inactive',
    lunarObsStatus: 'locked',
    workshopStatus: 'dormant',
    archiveStatus: 'sealed',
    villageMorale: 45,
    unresolvedConflicts: [
      'The ancient Mountain Springs of Elarion have gone bone-dry.',
      'A clockwork sentinel stands frozen at the Aqueduct sluice.',
      'The Moonstone Gate is locked by an unfulfilled condition.',
      'The Chasm of Echoes cannot be crossed without continuous light pulses.'
    ]
  });

  // Agent Telemetry
  const [telemetry, setTelemetry] = useState<AgentTelemetry[]>([
    { agent: 'DirectorAgent', role: 'Narrative Lead', output: 'Elarion campaign active. Awaiting hero action at Whispering Village.', status: 'approved' },
    { agent: 'LogicLearningAgent', role: 'Deterministic Validator', output: 'Computational thinking layer initialized across 6 progression levels.', status: 'verified' },
    { agent: 'WorldKeeperAgent', role: 'Continuity Laws', output: 'Elarion invariants locked: Spring channels dry until harmonic restoration.', status: 'verified' }
  ]);

  // The Codex of Becoming
  const [discoveries, setDiscoveries] = useState<DiscoveryItem[]>([
    {
      id: 'd-1',
      title: 'The Great Drought of Elarion',
      location: 'Whispering Village',
      lore: 'The mountain springs ceased flowing when the ancient resonance matrix fell out of harmonic alignment.',
      dateUnlocked: 'Session Start'
    }
  ]);

  const [scribedSpells, setScribedSpells] = useState<ScribedSpell[]>([]);

  // Epiphany Modal State
  const [activeEpiphany, setActiveEpiphany] = useState<EpiphanyReveal | null>(null);

  // -------------------------------------------------------------
  // LEVEL 1: SEQUENCE (The Clockwork Sentinel's Path)
  // -------------------------------------------------------------
  const [level1Steps, setLevel1Steps] = useState<string[]>([]);
  const [level1Status, setLevel1Status] = useState<'idle' | 'running' | 'success' | 'fail'>('idle');
  const [level1StepIndex, setLevel1StepIndex] = useState<number>(-1);
  const [level1Message, setLevel1Message] = useState<string>('');

  const addLevel1Step = (step: string) => {
    if (level1Steps.length < 5 && level1Status !== 'running') {
      setLevel1Steps([...level1Steps, step]);
    }
  };

  const removeLevel1Step = (idx: number) => {
    if (level1Status !== 'running') {
      setLevel1Steps(level1Steps.filter((_, i) => i !== idx));
    }
  };

  const runLevel1Simulation = () => {
    if (level1Steps.length === 0) {
      setLevel1Message('Please scribe at least one movement command for the sentinel.');
      setLevel1Status('fail');
      return;
    }

    setLevel1Status('running');
    setLevel1Message('The Clockwork Sentinel sputters to life and begins executing steps...');
    let currentIdx = 0;

    const interval = setInterval(() => {
      setLevel1StepIndex(currentIdx);
      currentIdx++;

      if (currentIdx > level1Steps.length) {
        clearInterval(interval);
        // Deterministic validation:
        // Expected sequence: ['STEP_FORWARD', 'STEP_FORWARD', 'TURN_RIGHT', 'STEP_FORWARD', 'ENGAGE_CLUTCH']
        const expected = ['STEP_FORWARD', 'STEP_FORWARD', 'TURN_RIGHT', 'STEP_FORWARD', 'ENGAGE_CLUTCH'];
        const isMatch =
          level1Steps.length === expected.length &&
          level1Steps.every((val, index) => val === expected[index]);

        if (isMatch) {
          setLevel1Status('success');
          setLevel1Message('Success! The sentinel reaches the altar, engages the bronze gear, and the sluice turns!');
          setWorld(prev => ({ ...prev, guardianStatus: 'operational', villageMorale: Math.min(100, prev.villageMorale + 10) }));
          setPlayer(prev => ({
            ...prev,
            challengeLevel: Math.max(prev.challengeLevel, 2),
            conceptMastery: { ...prev.conceptMastery, sequence: 100 }
          }));

          // Trigger Epiphany
          triggerEpiphany({
            primitive: 'ACTION',
            fantasyProblem: 'The clockwork sentinel must walk a precise path around stone pillars to turn the gear.',
            fantasySolution: 'You sequenced: Move Forward twice, pivot right, move forward, and engage clutch.',
            programmingConcept: 'Sequential Execution',
            explanation: 'In code, commands execute in strict top-to-bottom order. Swapping or skipping a command alters the entire outcome.',
            pythonSyntax: `# Sequential Execution\nsentinel.move_forward()\nsentinel.move_forward()\nsentinel.turn_right()\nsentinel.move_forward()\nsentinel.engage_clutch()`,
            javascriptSyntax: `// Sequential Execution\nsentinel.moveForward();\nsentinel.moveForward();\nsentinel.turnRight();\nsentinel.moveForward();\nsentinel.engageClutch();`
          });

          addDiscovery('The Sentinel Awakened', 'River Aqueduct', 'The bronze guardian responds to precise sequential kinetic commands.');
          addScribedSpell({
            name: 'Sentinel Kinetic Protocol',
            primitive: 'ACTION',
            fantasyIncantation: 'Pace forward twain, turn to the east gear, pace once, and mesh the clutch.',
            universalLogic: 'ACTION -> ACTION -> ACTION -> ACTION -> ACTION',
            pythonEquivalent: 'sentinel.walk(2); sentinel.turn(90); sentinel.walk(1); sentinel.act()',
            jsEquivalent: 'sentinel.walk(2).turn(90).walk(1).act()'
          });
        } else {
          setLevel1Status('fail');
          // Provide deterministic pedagogical hint
          if (level1Steps[0] !== 'STEP_FORWARD') {
            setLevel1Message('Hint: The sentinel immediately faces the stone path. It must first step forward towards the junction.');
          } else if (level1Steps[1] !== 'STEP_FORWARD') {
            setLevel1Message('Hint: The first turn is too early; a boulder blocks the direct turn. Take two paces forward first.');
          } else if (level1Steps[2] !== 'TURN_RIGHT') {
            setLevel1Message('Hint: At the junction, the sluice canal lies to the right.');
          } else if (level1Steps[3] !== 'STEP_FORWARD') {
            setLevel1Message('Hint: After turning, the sentinel is still one stone tile away from the gear mechanism.');
          } else if (level1Steps[4] !== 'ENGAGE_CLUTCH') {
            setLevel1Message('Hint: Reaching the dais is not enough; the sentinel must channel energy to engage the clutch.');
          } else {
            setLevel1Message('Hint: Check the length of your commands. Exactly 5 steps are needed to reach and engage.');
          }
        }
      }
    }, 550);
  };

  const resetLevel1 = () => {
    setLevel1Steps([]);
    setLevel1Status('idle');
    setLevel1StepIndex(-1);
    setLevel1Message('');
  };

  // -------------------------------------------------------------
  // LEVEL 2: CONDITIONS (The Moonstone Portal)
  // -------------------------------------------------------------
  const [level2MoonstoneLight, setLevel2MoonstoneLight] = useState<boolean>(false);
  const [level2OfferTribute, setLevel2OfferTribute] = useState<'none' | 'herb' | 'gem'>('none');
  const [level2Status, setLevel2Status] = useState<'idle' | 'success' | 'fail'>('idle');
  const [level2Message, setLevel2Message] = useState<string>('');

  const testLevel2Condition = () => {
    // Deterministic Rule:
    // The door opens ONLY IF the moonstone is glowing (true) AND an herb of peace is offered (herb)
    if (level2MoonstoneLight && level2OfferTribute === 'herb') {
      setLevel2Status('success');
      setLevel2Message('The Moonstone flares silver and the runic barrier dissolves! The Ancient Grove welcomes you.');
      setWorld(prev => ({ ...prev, spiritTrust: 10, villageMorale: Math.min(100, prev.villageMorale + 10) }));
      setPlayer(prev => ({
        ...prev,
        challengeLevel: Math.max(prev.challengeLevel, 3),
        conceptMastery: { ...prev.conceptMastery, conditions: 100 }
      }));

      triggerEpiphany({
        primitive: 'CONDITION',
        fantasyProblem: 'The portal gatekeeper checks if the sacred conditions are fulfilled before granting entry.',
        fantasySolution: 'You ensured: moonstone_is_glowing == True AND tribute == "herb".',
        programmingConcept: 'Conditional Branching (if / else)',
        explanation: 'Conditions evaluate to True or False. If the premise holds, one path executes; otherwise, another path is taken.',
        pythonSyntax: `# Conditional Evaluation\nif moonstone_is_glowing and tribute == "peace_herb":\n    portal.unlock()\n    print("Safe passage granted.")\nelse:\n    portal.remain_sealed()\n    print("The guardian runes repel entry.")`,
        javascriptSyntax: `// Conditional Evaluation\nif (moonstoneIsGlowing && tribute === "peace_herb") {\n    portal.unlock();\n    console.log("Safe passage granted.");\n} else {\n    portal.remainSealed();\n    console.log("The guardian runes repel entry.");\n}`
      });

      addDiscovery('The Moonstone Covenant', 'Ancient Grove', 'Runic gateways require exact environmental conditions before changing state.');
      addScribedSpell({
        name: 'Lunar Ward Passage',
        primitive: 'CONDITION',
        fantasyIncantation: 'If the celestial jewel shines radiant and peace is held, unseal the archway.',
        universalLogic: 'WHEN (moonstone == GLOWING && offering == PEACE) THEN UNLOCK ELSE REPEL',
        pythonEquivalent: 'if moonstone.is_glowing and offering == "herb": unlock()',
        jsEquivalent: 'if (moonstone.isGlowing && offering === "herb") { unlock(); }'
      });
    } else {
      setLevel2Status('fail');
      if (!level2MoonstoneLight && level2OfferTribute !== 'herb') {
        setLevel2Message('Failure: The moonstone is dark and no peace offering was laid on the altar.');
      } else if (!level2MoonstoneLight) {
        setLevel2Message('Failure: The grove guardian murmurs: "The stone is devoid of light. Kindle its luminescence."');
      } else {
        setLevel2Message('Failure: The moonstone shines, but the guardian warns: "Gold and iron are rejected. Only a soothing herb opens the archway."');
      }
    }
  };

  // -------------------------------------------------------------
  // LEVEL 3: LOOPS (The Enchanted Bridge of Light)
  // -------------------------------------------------------------
  const [level3RepetitionCount, setLevel3RepetitionCount] = useState<number>(3);
  const [level3Status, setLevel3Status] = useState<'idle' | 'running' | 'success' | 'fail'>('idle');
  const [level3ActiveTile, setLevel3ActiveTile] = useState<number>(-1);
  const [level3Message, setLevel3Message] = useState<string>('');

  const runLevel3BridgeSimulation = () => {
    setLevel3Status('running');
    setLevel3Message('Focusing crystal pulses into the floating bridge keystones...');

    let currentTile = 0;
    const maxSteps = level3RepetitionCount;

    const interval = setInterval(() => {
      setLevel3ActiveTile(currentTile);
      currentTile++;

      if (currentTile >= maxSteps) {
        clearInterval(interval);
        // Exactly 5 keystones required for the span of the chasm
        if (maxSteps === 5) {
          setLevel3Status('success');
          setLevel3Message('Harmonic Resonance! All 5 keystones solidify into radiant crystal. The bridge is permanently forged!');
          setWorld(prev => ({ ...prev, waterSupply: 'restoring', villageMorale: Math.min(100, prev.villageMorale + 15) }));
          setPlayer(prev => ({
            ...prev,
            challengeLevel: Math.max(prev.challengeLevel, 4),
            conceptMastery: { ...prev.conceptMastery, loops: 100 }
          }));

          triggerEpiphany({
            primitive: 'REPETITION',
            fantasyProblem: 'The Chasm of Echoes has five floating keystones that require identical continuous strikes to stabilize.',
            fantasySolution: 'You calibrated a repeating loop of exactly 5 pulse iterations.',
            programmingConcept: 'Loops & Iteration (for / while)',
            explanation: 'Loops allow a program to repeat the exact same set of instructions without manually writing them out 5 separate times.',
            pythonSyntax: `# Repetition via Loop\nfor keystone in range(1, 6):\n    crystallize_keystone(index=keystone)\n    print(f"Keystone {keystone} solidified.")\nprint("The bridge is complete!")`,
            javascriptSyntax: `// Repetition via Loop\nfor (let keystone = 1; keystone <= 5; keystone++) {\n    crystallizeKeystone(keystone);\n    console.log(\`Keystone \${keystone} solidified.\`);\n}\nconsole.log("The bridge is complete!");`
          });

          addDiscovery('The Span of Five Crystals', 'Clockwork Ruins', 'Chasm bridges demand repeated harmonic pulses to lock their resonance.');
          addScribedSpell({
            name: 'Pentaradial Harmonic Pulse',
            primitive: 'REPETITION',
            fantasyIncantation: 'Repeat the song of illumination fivefold until the fifth keystone locks.',
            universalLogic: 'REPEAT 5 TIMES: [STRIKE_KEYSTONE, SOLIDIFY]',
            pythonEquivalent: 'for i in range(5): strike_keystone(i)',
            jsEquivalent: 'for (let i = 0; i < 5; i++) { strikeKeystone(i); }'
          });
        } else if (maxSteps < 5) {
          setLevel3Status('fail');
          setLevel3Message(`The pulses ceased after only ${maxSteps} keystones. The bridge dissolved before reaching the other side! (Need 5).`);
        } else {
          setLevel3Status('fail');
          setLevel3Message(`You pulsed ${maxSteps} times! The excess energy overloaded the crystal lattice, causing the bridge to fracture. (Need exactly 5).`);
        }
      }
    }, 400);
  };

  // -------------------------------------------------------------
  // LEVEL 4: VARIABLES (The Moon Energy Cauldron)
  // -------------------------------------------------------------
  const [level4VialName, setLevel4VialName] = useState<'Aetherium' | 'PurifyingDew' | 'SolarEssence'>('Aetherium');
  const [level4EnergyValue, setLevel4EnergyValue] = useState<number>(20);
  const [level4Status, setLevel4Status] = useState<'idle' | 'success' | 'fail'>('idle');
  const [level4Message, setLevel4Message] = useState<string>('');

  const testLevel4Cauldron = () => {
    // Deterministic validation:
    // Required: Name = 'PurifyingDew' and Value between 50 and 65 (ideal 60)
    if (level4VialName === 'PurifyingDew' && level4EnergyValue >= 50 && level4EnergyValue <= 65) {
      setLevel4Status('success');
      setLevel4Message(`Masterful synthesis! The variable ${level4VialName} with energy magnitude ${level4EnergyValue} purifies the reservoir filters!`);
      setWorld(prev => ({ ...prev, lunarObsStatus: 'aligned', villageMorale: Math.min(100, prev.villageMorale + 15) }));
      setPlayer(prev => ({
        ...prev,
        challengeLevel: Math.max(prev.challengeLevel, 5),
        conceptMastery: { ...prev.conceptMastery, variables: 100 }
      }));

      triggerEpiphany({
        primitive: 'VALUE',
        fantasyProblem: 'The cauldron requires storing a dynamic energy quantity inside a specifically named celestial container.',
        fantasySolution: 'You defined: PurifyingDew = 60.',
        programmingConcept: 'Variables & Data Values',
        explanation: 'Variables are named storage containers that hold data values. We can change the value without changing the code structure.',
        pythonSyntax: `# Variable Assignment & Reading\nliquid_name = "PurifyingDew"\nenergy_level = 60\n\nif energy_level >= 50 and energy_level <= 65:\n    brew_result = "Purifying Elixir Synthesized"\n    print(f"{liquid_name} holds {energy_level} aether units.")`,
        javascriptSyntax: `// Variable Assignment & Reading\nlet liquidName = "PurifyingDew";\nlet energyLevel = 60;\n\nif (energyLevel >= 50 && energyLevel <= 65) {\n    let brewResult = "Purifying Elixir Synthesized";\n    console.log(\`\${liquidName} holds \${energyLevel} aether units.\`);\n}`
      });

      addDiscovery('The Reservoir Distillation', 'Lunar Observatory', 'Aetheric energy can be stored in named vessels with precise quantitative values.');
      addScribedSpell({
        name: 'Vessel of Pure Hydration',
        primitive: 'VALUE',
        fantasyIncantation: 'Bind sixty pulses of silver radiance under the name of Purifying Dew.',
        universalLogic: 'STORE (PurifyingDew := 60)',
        pythonEquivalent: 'purifying_dew = 60',
        jsEquivalent: 'const purifyingDew = 60;'
      });
    } else {
      setLevel4Status('fail');
      if (level4VialName !== 'PurifyingDew') {
        setLevel4Message(`The runes reject '${level4VialName}'. The ancient slate specifies: "Label the vessel as PurifyingDew."`);
      } else if (level4EnergyValue < 50) {
        setLevel4Message(`Energy level ${level4EnergyValue} is too weak. The brew remains inert (requires between 50 and 65).`);
      } else {
        setLevel4Message(`Energy level ${level4EnergyValue} is volatile! The cauldron bubbles violently (requires between 50 and 65).`);
      }
    }
  };

  // -------------------------------------------------------------
  // LEVEL 5: FUNCTIONS (The Scribing Glyph & Reusable Ritual)
  // -------------------------------------------------------------
  const [level5ElementArg, setLevel5ElementArg] = useState<'Frost' | 'Spark' | 'Terra'>('Frost');
  const [level5PowerArg, setLevel5PowerArg] = useState<number>(3);
  const [level5TestedPillars, setLevel5TestedPillars] = useState<{ frost: boolean; spark: boolean }>({
    frost: false,
    spark: false
  });
  const [level5Status, setLevel5Status] = useState<'idle' | 'success' | 'fail'>('idle');
  const [level5Message, setLevel5Message] = useState<string>('');

  const castLevel5Function = (target: 'Pillar of Ice' | 'Pillar of Lightning') => {
    if (target === 'Pillar of Ice') {
      if (level5ElementArg === 'Frost' && level5PowerArg >= 3) {
        setLevel5TestedPillars(prev => ({ ...prev, frost: true }));
        setLevel5Message('Frost glyph aligned with Pillar of Ice! Power 3+ stabilized the crystal matrix.');
      } else {
        setLevel5Message(`Failed: Pillar of Ice requires element "Frost" with power >= 3, but received ${level5ElementArg} (Power ${level5PowerArg}).`);
      }
    } else if (target === 'Pillar of Lightning') {
      if (level5ElementArg === 'Spark' && level5PowerArg >= 4) {
        setLevel5TestedPillars(prev => ({ ...prev, spark: true }));
        setLevel5Message('Spark glyph aligned with Pillar of Lightning! Power 4+ grounded the tempest.');
      } else {
        setLevel5Message(`Failed: Pillar of Lightning requires element "Spark" with power >= 4, but received ${level5ElementArg} (Power ${level5PowerArg}).`);
      }
    }
  };

  const evaluateLevel5Mastery = () => {
    if (level5TestedPillars.frost && level5TestedPillars.spark) {
      setLevel5Status('success');
      setLevel5Message('Marvelous! You reused the same parameterized function spell across multiple disparate pillars!');
      setWorld(prev => ({ ...prev, workshopStatus: 'ignited', villageMorale: Math.min(100, prev.villageMorale + 10) }));
      setPlayer(prev => ({
        ...prev,
        challengeLevel: Math.max(prev.challengeLevel, 6),
        conceptMastery: { ...prev.conceptMastery, functions: 100 }
      }));

      triggerEpiphany({
        primitive: 'REUSABLE_ACTION',
        fantasyProblem: 'Multiple varied pillars across the workshop need repair without inventing a separate spell for each.',
        fantasySolution: 'You created a single reusable spell function that takes (element, power) as parameters.',
        programmingConcept: 'Functions & Reusable Abstractions',
        explanation: 'A function bundles reusable logic into a named package. You define it once and call it anywhere with different inputs (parameters).',
        pythonSyntax: `# Function Definition with Parameters\ndef repair_pillar(pillar_name, element, power):\n    print(f"Channeling {power} units of {element} into {pillar_name}...")\n    return "Stabilized"\n\n# Reusing the function:\nrepair_pillar("Ice", "Frost", 3)\nrepair_pillar("Lightning", "Spark", 4)`,
        javascriptSyntax: `// Function Definition with Parameters\nfunction repairPillar(pillarName, element, power) {\n    console.log(\`Channeling \${power} units of \${element} into \${pillarName}...\`);\n    return "Stabilized";\n}\n\n// Reusing the function:\nrepairPillar("Ice", "Frost", 3);\nrepairPillar("Lightning", "Spark", 4);`
      });

      addDiscovery('The Archmage\'s Universal Scribe', 'Archmage\'s Workshop', 'A single incantation formula can adapt to any recipient via passing parameters.');
      addScribedSpell({
        name: 'Harmonic Scribing Function',
        primitive: 'REUSABLE_ACTION',
        fantasyIncantation: 'To repair any monument: invoke Glyph(element, power) with appropriate attributes.',
        universalLogic: 'FUNCTION repair(target, element, power) { INJECT(element, power); STABILIZE(); }',
        pythonEquivalent: 'def repair(target, element, power): stabilize(target, element, power)',
        jsEquivalent: 'function repair(target, element, power) { stabilize(target, element, power); }'
      });
    } else {
      setLevel5Status('fail');
      setLevel5Message('Both the Pillar of Ice and Pillar of Lightning must be successfully stabilized using your reusable glyph.');
    }
  };

  // -------------------------------------------------------------
  // LEVEL 6: DATA / COLLECTIONS (The Grand Celestial Archive)
  // -------------------------------------------------------------
  interface ArchiveRelic {
    id: string;
    name: string;
    element: 'Water' | 'Fire' | 'Aether' | 'Earth';
    power: number;
    status: 'Corrupted' | 'Pristine';
  }

  const archiveVault: ArchiveRelic[] = [
    { id: 'r1', name: 'Tear of Elarion', element: 'Water', power: 95, status: 'Pristine' },
    { id: 'r2', name: 'Ignis Ember', element: 'Fire', power: 80, status: 'Pristine' },
    { id: 'r3', name: 'Deepwell Pearl', element: 'Water', power: 88, status: 'Pristine' },
    { id: 'r4', name: 'Brine Shard', element: 'Water', power: 45, status: 'Corrupted' },
    { id: 'r5', name: 'Aether Lens', element: 'Aether', power: 90, status: 'Pristine' }
  ];

  const [level6ElementFilter, setLevel6ElementFilter] = useState<'All' | 'Water' | 'Fire' | 'Aether'>('All');
  const [level6MinPower, setLevel6MinPower] = useState<number>(85);
  const [level6PristineOnly, setLevel6PristineOnly] = useState<boolean>(true);
  const [level6Status, setLevel6Status] = useState<'idle' | 'success' | 'fail'>('idle');
  const [level6Message, setLevel6Message] = useState<string>('');

  const runLevel6ArchiveQuery = () => {
    // The riddle of the Master Spring:
    // "Only Pristine Water Relics with power >= 90 will unlock the Great Aqueduct Conduit."
    // Exactly matches 'Tear of Elarion'
    const filtered = archiveVault.filter(relic => {
      if (level6ElementFilter !== 'All' && relic.element !== level6ElementFilter) return false;
      if (relic.power < level6MinPower) return false;
      if (level6PristineOnly && relic.status !== 'Pristine') return false;
      return true;
    });

    const isCorrect =
      filtered.length === 1 &&
      filtered[0].id === 'r1' &&
      level6ElementFilter === 'Water' &&
      level6MinPower >= 90 &&
      level6PristineOnly;

    if (isCorrect) {
      setLevel6Status('success');
      setLevel6Message(`Vault Unsealed! Query yielded exactly [${filtered[0].name}] (Power: ${filtered[0].power}). The Master Spring rushes to life!`);
      setWorld(prev => ({
        ...prev,
        archiveStatus: 'opened',
        waterSupply: 'restored',
        villageMorale: 100,
        unresolvedConflicts: []
      }));
      setPlayer(prev => ({
        ...prev,
        challengeLevel: 6,
        conceptMastery: { ...prev.conceptMastery, collections: 100 }
      }));

      triggerEpiphany({
        primitive: 'COLLECTION',
        fantasyProblem: 'The Grand Archive contains hundreds of scattered enchanted relics. Finding the spring keystone by hand takes lifetimes.',
        fantasySolution: 'You filtered the collection: relics.filter(r => r.element == "Water" and r.power >= 90 and r.status == "Pristine").',
        programmingConcept: 'Collections, Lists & Data Structures',
        explanation: 'Collections store groups of related data. Programmers filter, search, and iterate through collections to extract exact answers effortlessly.',
        pythonSyntax: `# Filtering a List of Dictionaries\nrelics = [\n    {"name": "Tear of Elarion", "element": "Water", "power": 95},\n    {"name": "Deepwell Pearl", "element": "Water", "power": 88}\n]\n\n# List comprehension filter\nmaster_keys = [r for r in relics if r["element"] == "Water" and r["power"] >= 90]\nprint(f"Master Key found: {master_keys[0]['name']}")`,
        javascriptSyntax: `// Filtering an Array of Objects\nconst relics = [\n    { name: "Tear of Elarion", element: "Water", power: 95 },\n    { name: "Deepwell Pearl", element: "Water", power: 88 }\n];\n\n// Array filter\nconst masterKeys = relics.filter(r => r.element === "Water" && r.power >= 90);\nconsole.log(\`Master Key found: \${masterKeys[0].name}\`);`
      });

      addDiscovery('The Master Spring of Elarion', 'The Grand Archive', 'The ancient waters answer to the pure Water Relic extracted from the celestial collection.');
      addScribedSpell({
        name: 'Celestial Archive Sieve',
        primitive: 'COLLECTION',
        fantasyIncantation: 'From the vault of stars, gather only pristine water relics bearing power ninety and above.',
        universalLogic: 'COLLECTION.filter(item => item.element == "Water" && item.power >= 90 && item.isPristine)',
        pythonEquivalent: '[r for r in relics if r["element"] == "Water" and r["power"] >= 90]',
        jsEquivalent: 'relics.filter(r => r.element === "Water" && r.power >= 90)'
      });
    } else {
      setLevel6Status('fail');
      if (filtered.length === 0) {
        setLevel6Message('Your query returned 0 relics. Relax your constraints or check the element requirement.');
      } else if (filtered.some(r => r.element !== 'Water')) {
        setLevel6Message(`Your query returned non-water relics (${filtered.map(r => r.name).join(', ')}). The spring conduit only accepts Water.`);
      } else if (filtered.some(r => r.power < 90)) {
        setLevel6Message(`Your query included weak relics (${filtered.map(r => `${r.name}: ${r.power}`).join(', ')}). Only power >= 90 will trigger the valve.`);
      } else if (!level6PristineOnly) {
        setLevel6Message('Corrupted relics will poison the spring. Ensure Pristine Only is enforced.');
      } else {
        setLevel6Message(`The conduit requires the single supreme relic. Currently returned: ${filtered.length} items.`);
      }
    }
  };

  // Helper Functions
  const triggerEpiphany = (reveal: EpiphanyReveal) => {
    setActiveEpiphany(reveal);
    setTelemetry(prev => [
      {
        agent: 'LogicLearningAgent',
        role: 'Computational Thinking',
        output: `Epiphany unlocked: ${reveal.primitive} (${reveal.programmingConcept}). Evaluated deterministically.`,
        status: 'verified'
      },
      ...prev
    ]);
  };

  const addDiscovery = (title: string, location: string, lore: string) => {
    setDiscoveries(prev => {
      if (prev.some(d => d.title === title)) return prev;
      return [
        {
          id: `d-${Date.now()}`,
          title,
          location,
          lore,
          dateUnlocked: new Date().toLocaleTimeString()
        },
        ...prev
      ];
    });
  };

  const addScribedSpell = (spell: ScribedSpell) => {
    setScribedSpells(prev => {
      if (prev.some(s => s.name === spell.name)) return prev;
      return [spell, ...prev];
    });
  };

  const overallMasteryScore = Math.round(
    Object.values(player.conceptMastery).reduce((a, b) => a + b, 0) / 6
  );

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Epiphany Reveal Modal */}
      {activeEpiphany && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md animate-in fade-in duration-200">
          <div className="relative max-w-2xl w-full bg-slate-900 border-2 border-amber-500/60 rounded-2xl shadow-2xl p-6 md:p-8 space-y-6">
            <div className="flex items-center justify-between border-b border-amber-500/20 pb-4">
              <div className="flex items-center gap-3">
                <span className="p-2.5 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/30">
                  <Sparkles className="w-6 h-6 animate-pulse" />
                </span>
                <div>
                  <span className="text-[11px] font-mono tracking-widest text-amber-400 uppercase">
                    Epiphany Unlocked • {activeEpiphany.primitive}
                  </span>
                  <h2 className="text-2xl font-bold font-serif text-amber-100">
                    You just used a programming idea!
                  </h2>
                </div>
              </div>
              <button
                onClick={() => setActiveEpiphany(null)}
                className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                <div className="text-xs font-semibold text-amber-300 font-serif flex items-center gap-2">
                  <Compass className="w-4 h-4" /> In the Fantasy Realm:
                </div>
                <p className="text-sm text-slate-300 italic">{activeEpiphany.fantasyProblem}</p>
                <p className="text-xs text-emerald-400 font-mono">✦ {activeEpiphany.fantasySolution}</p>
              </div>

              <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-500/30 space-y-2">
                <div className="text-xs font-semibold text-amber-200 font-mono uppercase tracking-wider flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-amber-400" /> Computational Concept: {activeEpiphany.programmingConcept}
                </div>
                <p className="text-sm text-slate-200 leading-relaxed">{activeEpiphany.explanation}</p>
              </div>

              {/* Multi-Language Syntax Peek */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs text-slate-400">
                  <span className="font-mono">Real-World Code Mapping:</span>
                  <div className="flex gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800">
                    <button
                      onClick={() => setSelectedLanguageSyntax('python')}
                      className={`px-2 py-0.5 rounded text-[11px] font-mono transition ${
                        selectedLanguageSyntax === 'python'
                          ? 'bg-amber-500 text-slate-950 font-bold'
                          : 'text-slate-400 hover:text-white'
                      }`}
                    >
                      Python
                    </button>
                    <button
                      onClick={() => setSelectedLanguageSyntax('javascript')}
                      className={`px-2 py-0.5 rounded text-[11px] font-mono transition ${
                        selectedLanguageSyntax === 'javascript'
                          ? 'bg-amber-500 text-slate-950 font-bold'
                          : 'text-slate-400 hover:text-white'
                      }`}
                    >
                      JavaScript
                    </button>
                  </div>
                </div>

                <pre className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs font-mono text-amber-200 overflow-x-auto">
                  <code>
                    {selectedLanguageSyntax === 'python'
                      ? activeEpiphany.pythonSyntax
                      : activeEpiphany.javascriptSyntax}
                  </code>
                </pre>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => {
                  setActiveEpiphany(null);
                  setActiveTab('codex');
                }}
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-sm shadow-lg shadow-amber-500/20 flex items-center gap-2 transition"
              >
                Inscribe into Codex of Becoming <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Top Header */}
      <header className="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-40 px-4 lg:px-8 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-200 flex items-center justify-center text-slate-950 shadow-md shadow-amber-500/20 font-bold">
            ✨
          </div>
          <div>
            <h1 className="text-lg font-bold font-serif tracking-wide text-amber-100 flex items-center gap-2">
              MythCode
              <span className="text-[10px] font-sans font-semibold px-2 py-0.5 bg-amber-500/10 text-amber-400 border border-amber-500/30 rounded-full">
                Experiential Learning
              </span>
            </h1>
            <p className="text-[11px] text-slate-400 font-sans">
              Kingdom of {world.kingdom} • Springs of Elarion
            </p>
          </div>
        </div>

        {/* Global Progress Bar */}
        <div className="hidden md:flex items-center gap-4 bg-slate-950/80 px-4 py-1.5 rounded-xl border border-slate-800">
          <div className="text-right">
            <span className="text-[10px] uppercase font-mono text-slate-400 block">Computational Awakening</span>
            <span className="text-xs font-bold font-mono text-amber-300">{overallMasteryScore}% Mastered</span>
          </div>
          <div className="w-32 h-2.5 bg-slate-800 rounded-full overflow-hidden border border-slate-700">
            <div
              className="h-full bg-gradient-to-r from-amber-500 to-emerald-400 transition-all duration-500"
              style={{ width: `${overallMasteryScore}%` }}
            />
          </div>
        </div>

        {/* Nav Tabs */}
        <nav className="flex items-center gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('adventure')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activeTab === 'adventure'
                ? 'bg-amber-500/20 text-amber-200 border border-amber-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Compass className="w-3.5 h-3.5" />
            <span>Adventure</span>
          </button>

          <button
            onClick={() => setActiveTab('challenges')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activeTab === 'challenges'
                ? 'bg-amber-500/20 text-amber-200 border border-amber-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Zap className="w-3.5 h-3.5 text-amber-400" />
            <span>Trials ({player.challengeLevel}/6)</span>
          </button>

          <button
            onClick={() => setActiveTab('codex')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activeTab === 'codex'
                ? 'bg-amber-500/20 text-amber-200 border border-amber-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 text-amber-300" />
            <span>The Codex</span>
          </button>

          <button
            onClick={() => setActiveTab('world')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activeTab === 'world'
                ? 'bg-amber-500/20 text-amber-200 border border-amber-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Droplets className="w-3.5 h-3.5 text-sky-400" />
            <span>Elarion</span>
          </button>

          <button
            onClick={() => setActiveTab('agents')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 ${
              activeTab === 'agents'
                ? 'bg-amber-500/20 text-amber-200 border border-amber-500/40'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Cpu className="w-3.5 h-3.5 text-purple-400" />
            <span>Agents</span>
          </button>
        </nav>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 lg:p-8 space-y-6">

        {/* ---------------------------------------------------------------- */}
        {/* TAB 1: ADVENTURE & STORY WORLD */}
        {/* ---------------------------------------------------------------- */}
        {activeTab === 'adventure' && (
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Story Panel */}
            <div className="lg:col-span-2 space-y-6">
              <div className="bg-slate-900/90 border border-amber-500/30 rounded-2xl p-6 md:p-8 shadow-xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-64 h-64 bg-amber-500/5 rounded-full blur-3xl pointer-events-none" />

                <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
                  <span className="text-xs font-mono text-amber-400 uppercase tracking-widest flex items-center gap-2">
                    <Compass className="w-4 h-4" /> Current Location: {world.location}
                  </span>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono">
                    Spring Status: {world.waterSupply.toUpperCase()}
                  </span>
                </div>

                <div className="space-y-4">
                  <h2 className="text-2xl md:text-3xl font-serif font-bold text-amber-100">
                    {world.location === 'Whispering Village' && 'The Silent Village Square'}
                    {world.location === 'River Aqueduct' && 'The Sluice Gate of the Sentinel'}
                    {world.location === 'Ancient Grove' && 'The Misty Moonstone Threshold'}
                    {world.location === 'Clockwork Ruins' && 'The Chasm of Echoes'}
                    {world.location === 'Lunar Observatory' && 'The Celestial Distillation Vault'}
                    {world.location === 'Archmage Workshop' && 'The Hall of Fractured Pillars'}
                    {world.location === 'Grand Archive' && 'The Grand Celestial Vault'}
                  </h2>

                  <p className="text-slate-300 leading-relaxed font-serif text-lg">
                    {world.location === 'Whispering Village' &&
                      'The central fountain lies bone-dry, its cracked stone basin carpeted in fallen leaves. Elder Thorne wrings his hands as villagers look toward the dry mountain aqueducts. "Our springs have slumbered for seasons," Thorne pleads. "Solve the ancient mechanism at the river, and awaken the dormant sentinel!"'}

                    {world.location === 'River Aqueduct' &&
                      'Massive bronze gears hang motionless over the dried canal. Beside the altar stands the Clockwork Sentinel. Mira the Artificer observes: "The gear cannot be turned by hand. You must sequence the kinetic steps into the sentinel dais to walk it to the clutch!"'}

                    {world.location === 'Ancient Grove' &&
                      'Bioluminescent flora illuminates a giant mossy archway. Sylvan the Forest Warden watches from the shadows. "None may enter the upper mountains unless the Moonstone condition is satisfied. Light the stone and bear the peaceful tribute, traveler!"'}

                    {world.location === 'Clockwork Ruins' &&
                      'A bottomless fissure splits the stone hall. Five floating crystal keystones hover in the abyss. An echo rings out: "A single pulse will not hold. Only a repeated harmonic loop of five pulses will crystallize the bridge of light."'}

                    {world.location === 'Lunar Observatory' &&
                      'Celestial mirrors focus moonbeams into a glass condenser. "To purify the reservoir springs," reads an engraved tablet, "you must store the exact quantity of moon energy inside the PurifyingDew vessel."'}

                    {world.location === 'Archmage Workshop' &&
                      'Multiple elemental pillars hum irregularly. "Do not craft individual rites for every spire," reads the archmage\'s journal. "Carve a single reusable glyph that accepts the element and power level as its parameters."'}

                    {world.location === 'Grand Archive' &&
                      'Shelves of floating relics span as far as the eye can see. "The Master Spring Valve responds solely to the pristine Water relic with power greater than ninety. Query the collection to claim the key!"'}
                  </p>
                </div>

                {/* Narrative Action Choices */}
                <div className="mt-8 pt-6 border-t border-slate-800 space-y-3">
                  <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400">
                    Seek Adventure & Face Fantasy Problems:
                  </h4>
                  <div className="grid sm:grid-cols-2 gap-3">
                    <button
                      onClick={() => {
                        setWorld(prev => ({ ...prev, location: 'River Aqueduct' }));
                        setActiveTab('challenges');
                      }}
                      className="p-3 rounded-xl bg-slate-950 border border-slate-800 hover:border-amber-500/50 hover:bg-slate-800 text-left transition flex items-center justify-between group"
                    >
                      <div>
                        <div className="text-sm font-semibold text-amber-200 group-hover:text-amber-300">
                          1. Guide the Aqueduct Sentinel
                        </div>
                        <div className="text-[11px] text-slate-400">Sequence Challenge</div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-amber-400 group-hover:translate-x-1 transition" />
                    </button>

                    <button
                      onClick={() => {
                        setWorld(prev => ({ ...prev, location: 'Ancient Grove' }));
                        setActiveTab('challenges');
                      }}
                      className="p-3 rounded-xl bg-slate-950 border border-slate-800 hover:border-amber-500/50 hover:bg-slate-800 text-left transition flex items-center justify-between group"
                    >
                      <div>
                        <div className="text-sm font-semibold text-amber-200 group-hover:text-amber-300">
                          2. Unlock Moonstone Archway
                        </div>
                        <div className="text-[11px] text-slate-400">Condition Challenge</div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-amber-400 group-hover:translate-x-1 transition" />
                    </button>

                    <button
                      onClick={() => {
                        setWorld(prev => ({ ...prev, location: 'Clockwork Ruins' }));
                        setActiveTab('challenges');
                      }}
                      className="p-3 rounded-xl bg-slate-950 border border-slate-800 hover:border-amber-500/50 hover:bg-slate-800 text-left transition flex items-center justify-between group"
                    >
                      <div>
                        <div className="text-sm font-semibold text-amber-200 group-hover:text-amber-300">
                          3. Cross the Chasm of Echoes
                        </div>
                        <div className="text-[11px] text-slate-400">Loop Challenge</div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-amber-400 group-hover:translate-x-1 transition" />
                    </button>

                    <button
                      onClick={() => {
                        setWorld(prev => ({ ...prev, location: 'Lunar Observatory' }));
                        setActiveTab('challenges');
                      }}
                      className="p-3 rounded-xl bg-slate-950 border border-slate-800 hover:border-amber-500/50 hover:bg-slate-800 text-left transition flex items-center justify-between group"
                    >
                      <div>
                        <div className="text-sm font-semibold text-amber-200 group-hover:text-amber-300">
                          4. Distill Moon Energy Cauldron
                        </div>
                        <div className="text-[11px] text-slate-400">Variable Challenge</div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-amber-400 group-hover:translate-x-1 transition" />
                    </button>

                    <button
                      onClick={() => {
                        setWorld(prev => ({ ...prev, location: 'Archmage Workshop' }));
                        setActiveTab('challenges');
                      }}
                      className="p-3 rounded-xl bg-slate-950 border border-slate-800 hover:border-amber-500/50 hover:bg-slate-800 text-left transition flex items-center justify-between group"
                    >
                      <div>
                        <div className="text-sm font-semibold text-amber-200 group-hover:text-amber-300">
                          5. Reusable Pillar Inscription
                        </div>
                        <div className="text-[11px] text-slate-400">Function Challenge</div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-amber-400 group-hover:translate-x-1 transition" />
                    </button>

                    <button
                      onClick={() => {
                        setWorld(prev => ({ ...prev, location: 'Grand Archive' }));
                        setActiveTab('challenges');
                      }}
                      className="p-3 rounded-xl bg-slate-950 border border-slate-800 hover:border-amber-500/50 hover:bg-slate-800 text-left transition flex items-center justify-between group"
                    >
                      <div>
                        <div className="text-sm font-semibold text-amber-200 group-hover:text-amber-300">
                          6. Sieve the Celestial Relics
                        </div>
                        <div className="text-[11px] text-slate-400">Collections Challenge</div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-amber-400 group-hover:translate-x-1 transition" />
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Sidebar Profile & World Status */}
            <div className="space-y-6">
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-slate-800 border border-amber-500/30 flex items-center justify-center text-amber-300 font-bold text-lg">
                    {player.name[0]}
                  </div>
                  <div>
                    <h3 className="font-serif font-bold text-amber-100">{player.name}</h3>
                    <p className="text-xs text-slate-400 font-sans">{player.role} • Level {player.challengeLevel}</p>
                  </div>
                </div>

                <div className="space-y-2 border-t border-slate-800 pt-4 text-xs font-mono">
                  <div className="flex justify-between text-slate-300">
                    <span>Village Morale:</span>
                    <span className="text-emerald-400 font-bold">{world.villageMorale}%</span>
                  </div>
                  <div className="flex justify-between text-slate-300">
                    <span>Spirit Trust:</span>
                    <span className="text-sky-400 font-bold">{world.spiritTrust}/10</span>
                  </div>
                  <div className="flex justify-between text-slate-300">
                    <span>Spring Water Flow:</span>
                    <span className="text-amber-300 font-bold capitalize">{world.waterSupply}</span>
                  </div>
                </div>

                <div className="border-t border-slate-800 pt-4">
                  <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider block mb-2">
                    Active World Conflicts:
                  </span>
                  {world.unresolvedConflicts.length > 0 ? (
                    <ul className="space-y-1.5 text-xs text-amber-200/80">
                      {world.unresolvedConflicts.map((c, idx) => (
                        <li key={idx} className="flex items-start gap-1.5">
                          <span className="text-amber-400 mt-0.5">•</span>
                          <span>{c}</span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <div className="p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-xl text-emerald-300 text-xs font-sans">
                      All conflicts resolved! The mountain springs of Elarion flow with vibrant crystal water.
                    </div>
                  )}
                </div>
              </div>

              {/* Quick Codex Preview */}
              <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="font-serif font-bold text-amber-200 text-sm flex items-center gap-2">
                    <BookOpen className="w-4 h-4 text-amber-400" /> Codex of Becoming
                  </h4>
                  <span className="text-[10px] font-mono text-slate-400">{discoveries.length} Discoveries</span>
                </div>
                <p className="text-xs text-slate-400">
                  Your achievements and computational spells are recorded as world discoveries.
                </p>
                <button
                  onClick={() => setActiveTab('codex')}
                  className="w-full py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-amber-200 transition"
                >
                  Open Scribed Entries &rarr;
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ---------------------------------------------------------------- */}
        {/* TAB 2: PROGRESSIVE FANTASY LEARNING TRIALS */}
        {/* ---------------------------------------------------------------- */}
        {activeTab === 'challenges' && (
          <div className="space-y-8">
            <div className="bg-slate-900/90 border border-amber-500/30 rounded-2xl p-6 shadow-xl">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
                <div>
                  <span className="text-xs font-mono text-amber-400 uppercase tracking-widest">
                    Experiential Computational Progression
                  </span>
                  <h2 className="text-2xl font-serif font-bold text-amber-100">
                    The Six Harmonic Trials of Elarion
                  </h2>
                </div>
                <div className="flex items-center gap-2 text-xs font-mono text-slate-400 bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-800">
                  <Shield className="w-4 h-4 text-emerald-400" />
                  <span>Deterministic Validation Active</span>
                </div>
              </div>
              <p className="text-xs text-slate-400 mt-3 font-sans max-w-3xl">
                Solve the fantasy crisis using the world's magical mechanisms. Experiment freely without penalty.
                The game verifies your solution using pure deterministic logic, and reveals the computational insight upon success!
              </p>
            </div>

            {/* LEVEL 1: SEQUENCE */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 space-y-6 shadow-xl">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[11px] font-mono px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30 uppercase">
                    Level 1 • Order of Enchantment
                  </span>
                  <h3 className="text-xl font-bold font-serif text-amber-100 mt-2">
                    The Clockwork Sentinel's Stepping Path
                  </h3>
                  <p className="text-xs text-slate-400 font-sans mt-1">
                    "Do these magical actions in the exact correct order." The sentinel must navigate the stone tiles to reach the sluice clutch.
                  </p>
                </div>
                {player.conceptMastery.sequence === 100 && (
                  <span className="px-3 py-1 rounded-full bg-emerald-950 border border-emerald-500/30 text-emerald-400 text-xs font-mono flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Solved
                  </span>
                )}
              </div>

              {/* Visual Grid Simulation */}
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-4">
                <div className="text-xs font-mono text-slate-400 flex items-center justify-between">
                  <span>Interactive Dais: Stepping Sequence ({level1Steps.length}/5)</span>
                  <button
                    onClick={resetLevel1}
                    className="text-xs text-slate-400 hover:text-white flex items-center gap-1"
                  >
                    <RotateCcw className="w-3.5 h-3.5" /> Reset
                  </button>
                </div>

                {/* Steps Display */}
                <div className="min-h-14 p-2 rounded-lg bg-slate-900 border border-slate-800 flex items-center gap-2 overflow-x-auto">
                  {level1Steps.length === 0 ? (
                    <span className="text-xs text-slate-500 italic p-2">Click movement commands below to scribe the order...</span>
                  ) : (
                    level1Steps.map((step, idx) => (
                      <div
                        key={idx}
                        className={`px-3 py-1.5 rounded-lg text-xs font-mono flex items-center gap-2 border transition ${
                          level1StepIndex === idx
                            ? 'bg-amber-500 text-slate-950 font-bold border-amber-400 shadow-md shadow-amber-500/30'
                            : 'bg-slate-950 text-amber-200 border-slate-700'
                        }`}
                      >
                        <span>{idx + 1}. {step.replace('_', ' ')}</span>
                        {level1Status !== 'running' && (
                          <button
                            onClick={() => removeLevel1Step(idx)}
                            className="text-slate-500 hover:text-red-400 text-xs ml-1"
                          >
                            ×
                          </button>
                        )}
                      </div>
                    ))
                  )}
                </div>

                {/* Available Action Buttons */}
                <div className="flex flex-wrap gap-2 pt-2">
                  <button
                    onClick={() => addLevel1Step('STEP_FORWARD')}
                    disabled={level1Status === 'running' || level1Steps.length >= 5}
                    className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-medium text-slate-200 transition disabled:opacity-50"
                  >
                    + Step Forward
                  </button>
                  <button
                    onClick={() => addLevel1Step('TURN_RIGHT')}
                    disabled={level1Status === 'running' || level1Steps.length >= 5}
                    className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-medium text-slate-200 transition disabled:opacity-50"
                  >
                    + Turn 90° Right
                  </button>
                  <button
                    onClick={() => addLevel1Step('TURN_LEFT')}
                    disabled={level1Status === 'running' || level1Steps.length >= 5}
                    className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-medium text-slate-200 transition disabled:opacity-50"
                  >
                    + Turn 90° Left
                  </button>
                  <button
                    onClick={() => addLevel1Step('ENGAGE_CLUTCH')}
                    disabled={level1Status === 'running' || level1Steps.length >= 5}
                    className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-medium text-slate-200 transition disabled:opacity-50"
                  >
                    + Engage Gear Clutch
                  </button>
                </div>

                {/* Run Simulation Button & Result */}
                <div className="pt-2 flex items-center justify-between border-t border-slate-800">
                  <div className="text-xs">
                    {level1Status === 'fail' && (
                      <span className="text-amber-400 font-sans flex items-center gap-1.5">
                        <AlertCircle className="w-4 h-4" /> {level1Message}
                      </span>
                    )}
                    {level1Status === 'success' && (
                      <span className="text-emerald-400 font-sans flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4" /> {level1Message}
                      </span>
                    )}
                    {level1Status === 'running' && (
                      <span className="text-slate-300 font-mono animate-pulse">{level1Message}</span>
                    )}
                  </div>
                  <button
                    onClick={runLevel1Simulation}
                    disabled={level1Status === 'running'}
                    className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-md shadow-amber-500/20 transition disabled:opacity-50"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" /> Execute Sequence
                  </button>
                </div>
              </div>
            </div>

            {/* LEVEL 2: CONDITIONS */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 space-y-6 shadow-xl">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[11px] font-mono px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30 uppercase">
                    Level 2 • Truth of the Threshold
                  </span>
                  <h3 className="text-xl font-bold font-serif text-amber-100 mt-2">
                    The Moonstone Portal of the Ancient Grove
                  </h3>
                  <p className="text-xs text-slate-400 font-sans mt-1">
                    "The door opens only if the moonstone is glowing and an offering of peace is made."
                  </p>
                </div>
                {player.conceptMastery.conditions === 100 && (
                  <span className="px-3 py-1 rounded-full bg-emerald-950 border border-emerald-500/30 text-emerald-400 text-xs font-mono flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Solved
                  </span>
                )}
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  {/* Moonstone State Toggle */}
                  <div className="p-4 rounded-lg bg-slate-900 border border-slate-800 space-y-2">
                    <div className="text-xs font-mono text-slate-400">Condition 1: Moonstone State</div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-serif text-slate-200">
                        {level2MoonstoneLight ? 'Radiant Luminescence (Glowing)' : 'Dormant Shadow (Dark)'}
                      </span>
                      <button
                        onClick={() => setLevel2MoonstoneLight(!level2MoonstoneLight)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                          level2MoonstoneLight
                            ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20'
                            : 'bg-slate-800 text-slate-300'
                        }`}
                      >
                        {level2MoonstoneLight ? 'Glowing (True)' : 'Dark (False)'}
                      </button>
                    </div>
                  </div>

                  {/* Altar Tribute Selection */}
                  <div className="p-4 rounded-lg bg-slate-900 border border-slate-800 space-y-2">
                    <div className="text-xs font-mono text-slate-400">Condition 2: Altar Tribute</div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => setLevel2OfferTribute('herb')}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                          level2OfferTribute === 'herb'
                            ? 'bg-amber-500 text-slate-950 font-bold'
                            : 'bg-slate-800 text-slate-300'
                        }`}
                      >
                        Peace Herb
                      </button>
                      <button
                        onClick={() => setLevel2OfferTribute('gem')}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                          level2OfferTribute === 'gem'
                            ? 'bg-amber-500 text-slate-950 font-bold'
                            : 'bg-slate-800 text-slate-300'
                        }`}
                      >
                        Gold Gem
                      </button>
                      <button
                        onClick={() => setLevel2OfferTribute('none')}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                          level2OfferTribute === 'none'
                            ? 'bg-amber-500 text-slate-950 font-bold'
                            : 'bg-slate-800 text-slate-300'
                        }`}
                      >
                        None
                      </button>
                    </div>
                  </div>
                </div>

                <div className="pt-2 flex items-center justify-between border-t border-slate-800">
                  <div className="text-xs">
                    {level2Status === 'fail' && (
                      <span className="text-amber-400 font-sans flex items-center gap-1.5">
                        <AlertCircle className="w-4 h-4" /> {level2Message}
                      </span>
                    )}
                    {level2Status === 'success' && (
                      <span className="text-emerald-400 font-sans flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4" /> {level2Message}
                      </span>
                    )}
                  </div>
                  <button
                    onClick={testLevel2Condition}
                    className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-md shadow-amber-500/20 transition"
                  >
                    Test Gate Condition &rarr;
                  </button>
                </div>
              </div>
            </div>

            {/* LEVEL 3: LOOPS */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 space-y-6 shadow-xl">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[11px] font-mono px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30 uppercase">
                    Level 3 • Repeating Incantation
                  </span>
                  <h3 className="text-xl font-bold font-serif text-amber-100 mt-2">
                    The Enchanted Bridge of Light
                  </h3>
                  <p className="text-xs text-slate-400 font-sans mt-1">
                    "The enchanted bridge requires the exact same pulse five times to anchor the floating keystones."
                  </p>
                </div>
                {player.conceptMastery.loops === 100 && (
                  <span className="px-3 py-1 rounded-full bg-emerald-950 border border-emerald-500/30 text-emerald-400 text-xs font-mono flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Solved
                  </span>
                )}
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-4">
                {/* 5 Keystones Visualizer */}
                <div className="grid grid-cols-5 gap-2 py-4">
                  {[0, 1, 2, 3, 4].map(idx => (
                    <div
                      key={idx}
                      className={`h-16 rounded-xl border flex flex-col items-center justify-center transition-all duration-300 ${
                        level3ActiveTile >= idx
                          ? 'bg-sky-500/20 border-sky-400 shadow-lg shadow-sky-500/30 text-sky-200'
                          : 'bg-slate-900 border-slate-800 text-slate-600'
                      }`}
                    >
                      <Sparkles className={`w-5 h-5 mb-1 ${level3ActiveTile >= idx ? 'animate-pulse text-sky-400' : ''}`} />
                      <span className="text-[11px] font-mono">Keystone #{idx + 1}</span>
                    </div>
                  ))}
                </div>

                {/* Loop Calibrator Slider */}
                <div className="p-4 rounded-lg bg-slate-900 border border-slate-800 space-y-2">
                  <div className="flex justify-between text-xs font-mono text-slate-300">
                    <span>Harmonic Loop Iteration Count:</span>
                    <span className="text-amber-400 font-bold">{level3RepetitionCount} Cycles</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="8"
                    value={level3RepetitionCount}
                    onChange={e => setLevel3RepetitionCount(parseInt(e.target.value))}
                    disabled={level3Status === 'running'}
                    className="w-full accent-amber-500 cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                    <span>1 (Weak)</span>
                    <span>5 (Chasm Span)</span>
                    <span>8 (Overload)</span>
                  </div>
                </div>

                <div className="pt-2 flex items-center justify-between border-t border-slate-800">
                  <div className="text-xs">
                    {level3Status === 'fail' && (
                      <span className="text-amber-400 font-sans flex items-center gap-1.5">
                        <AlertCircle className="w-4 h-4" /> {level3Message}
                      </span>
                    )}
                    {level3Status === 'success' && (
                      <span className="text-emerald-400 font-sans flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4" /> {level3Message}
                      </span>
                    )}
                    {level3Status === 'running' && (
                      <span className="text-sky-400 font-mono animate-pulse">{level3Message}</span>
                    )}
                  </div>
                  <button
                    onClick={runLevel3BridgeSimulation}
                    disabled={level3Status === 'running'}
                    className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-md shadow-amber-500/20 transition disabled:opacity-50"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" /> Fire Repeating Loop
                  </button>
                </div>
              </div>
            </div>

            {/* LEVEL 4: VARIABLES */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 space-y-6 shadow-xl">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[11px] font-mono px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30 uppercase">
                    Level 4 • Containers of Power
                  </span>
                  <h3 className="text-xl font-bold font-serif text-amber-100 mt-2">
                    The Moon Energy Cauldron
                  </h3>
                  <p className="text-xs text-slate-400 font-sans mt-1">
                    "The amount of moon energy stored inside the named vessel determines the purification spell."
                  </p>
                </div>
                {player.conceptMastery.variables === 100 && (
                  <span className="px-3 py-1 rounded-full bg-emerald-950 border border-emerald-500/30 text-emerald-400 text-xs font-mono flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Solved
                  </span>
                )}
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  {/* Named Variable Container */}
                  <div className="p-4 rounded-lg bg-slate-900 border border-slate-800 space-y-2">
                    <span className="text-xs font-mono text-slate-400 block">Vessel Name Identifier:</span>
                    <select
                      value={level4VialName}
                      onChange={e => setLevel4VialName(e.target.value as any)}
                      className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs font-mono text-amber-200"
                    >
                      <option value="Aetherium">Aetherium (Raw Ore)</option>
                      <option value="PurifyingDew">PurifyingDew (Filter Reagent)</option>
                      <option value="SolarEssence">SolarEssence (Combustion)</option>
                    </select>
                  </div>

                  {/* Value Slider */}
                  <div className="p-4 rounded-lg bg-slate-900 border border-slate-800 space-y-2">
                    <div className="flex justify-between text-xs font-mono text-slate-300">
                      <span>Stored Energy Magnitude:</span>
                      <span className="text-amber-400 font-bold">{level4EnergyValue} Units</span>
                    </div>
                    <input
                      type="range"
                      min="10"
                      max="100"
                      value={level4EnergyValue}
                      onChange={e => setLevel4EnergyValue(parseInt(e.target.value))}
                      className="w-full accent-amber-500 cursor-pointer"
                    />
                    <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                      <span>10 (Inert)</span>
                      <span>50-65 (Purifying Zone)</span>
                      <span>100 (Volatile)</span>
                    </div>
                  </div>
                </div>

                <div className="pt-2 flex items-center justify-between border-t border-slate-800">
                  <div className="text-xs">
                    {level4Status === 'fail' && (
                      <span className="text-amber-400 font-sans flex items-center gap-1.5">
                        <AlertCircle className="w-4 h-4" /> {level4Message}
                      </span>
                    )}
                    {level4Status === 'success' && (
                      <span className="text-emerald-400 font-sans flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4" /> {level4Message}
                      </span>
                    )}
                  </div>
                  <button
                    onClick={testLevel4Cauldron}
                    className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-md shadow-amber-500/20 transition"
                  >
                    Distill Cauldron Brew &rarr;
                  </button>
                </div>
              </div>
            </div>

            {/* LEVEL 5: FUNCTIONS */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 space-y-6 shadow-xl">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[11px] font-mono px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30 uppercase">
                    Level 5 • Scribing Reusable Glyphs
                  </span>
                  <h3 className="text-xl font-bold font-serif text-amber-100 mt-2">
                    The Universal Pillar Restoration Spell
                  </h3>
                  <p className="text-xs text-slate-400 font-sans mt-1">
                    "You have discovered a reusable spell formula. Pass parameters (element, power) to heal both damaged pillars."
                  </p>
                </div>
                {player.conceptMastery.functions === 100 && (
                  <span className="px-3 py-1 rounded-full bg-emerald-950 border border-emerald-500/30 text-emerald-400 text-xs font-mono flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Solved
                  </span>
                )}
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-4">
                {/* Pillar Status Tracker */}
                <div className="grid md:grid-cols-2 gap-4">
                  <div className={`p-4 rounded-xl border space-y-2 transition ${
                    level5TestedPillars.frost
                      ? 'bg-sky-950/40 border-sky-500/40 text-sky-200'
                      : 'bg-slate-900 border-slate-800 text-slate-400'
                  }`}>
                    <div className="flex justify-between items-center text-xs font-mono">
                      <span>Target: Pillar of Ice</span>
                      {level5TestedPillars.frost ? (
                        <span className="text-emerald-400 font-bold">STABILIZED</span>
                      ) : (
                        <span className="text-amber-400">REQUIRES FROST &gt;= 3</span>
                      )}
                    </div>
                    <button
                      onClick={() => castLevel5Function('Pillar of Ice')}
                      className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-mono transition"
                    >
                      Call restoreGlyph(&quot;Ice&quot;, {level5ElementArg}, {level5PowerArg})
                    </button>
                  </div>

                  <div className={`p-4 rounded-xl border space-y-2 transition ${
                    level5TestedPillars.spark
                      ? 'bg-amber-950/40 border-amber-500/40 text-amber-200'
                      : 'bg-slate-900 border-slate-800 text-slate-400'
                  }`}>
                    <div className="flex justify-between items-center text-xs font-mono">
                      <span>Target: Pillar of Lightning</span>
                      {level5TestedPillars.spark ? (
                        <span className="text-emerald-400 font-bold">STABILIZED</span>
                      ) : (
                        <span className="text-amber-400">REQUIRES SPARK &gt;= 4</span>
                      )}
                    </div>
                    <button
                      onClick={() => castLevel5Function('Pillar of Lightning')}
                      className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-mono transition"
                    >
                      Call restoreGlyph(&quot;Lightning&quot;, {level5ElementArg}, {level5PowerArg})
                    </button>
                  </div>
                </div>

                {/* Function Parameter Inputs */}
                <div className="p-4 rounded-lg bg-slate-900 border border-slate-800 grid md:grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <span className="text-xs font-mono text-slate-400">Parameter 1: Element</span>
                    <div className="flex gap-2">
                      {(['Frost', 'Spark', 'Terra'] as const).map(elem => (
                        <button
                          key={elem}
                          onClick={() => setLevel5ElementArg(elem)}
                          className={`px-3 py-1.5 rounded-lg text-xs font-mono transition ${
                            level5ElementArg === elem
                              ? 'bg-amber-500 text-slate-950 font-bold'
                              : 'bg-slate-950 text-slate-300'
                          }`}
                        >
                          {elem}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="space-y-1">
                    <div className="flex justify-between text-xs font-mono text-slate-400">
                      <span>Parameter 2: Power</span>
                      <span className="text-amber-300 font-bold">{level5PowerArg} Units</span>
                    </div>
                    <input
                      type="range"
                      min="1"
                      max="6"
                      value={level5PowerArg}
                      onChange={e => setLevel5PowerArg(parseInt(e.target.value))}
                      className="w-full accent-amber-500 cursor-pointer"
                    />
                  </div>
                </div>

                <div className="pt-2 flex items-center justify-between border-t border-slate-800">
                  <div className="text-xs">
                    {level5Status === 'fail' && (
                      <span className="text-amber-400 font-sans flex items-center gap-1.5">
                        <AlertCircle className="w-4 h-4" /> {level5Message}
                      </span>
                    )}
                    {level5Status === 'success' && (
                      <span className="text-emerald-400 font-sans flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4" /> {level5Message}
                      </span>
                    )}
                    {level5Status === 'idle' && level5Message && (
                      <span className="text-slate-300 font-sans">{level5Message}</span>
                    )}
                  </div>
                  <button
                    onClick={evaluateLevel5Mastery}
                    className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-md shadow-amber-500/20 transition"
                  >
                    Confirm Both Pillars Healed &rarr;
                  </button>
                </div>
              </div>
            </div>

            {/* LEVEL 6: COLLECTIONS */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 space-y-6 shadow-xl">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[11px] font-mono px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30 uppercase">
                    Level 6 • Sieve of the Archives
                  </span>
                  <h3 className="text-xl font-bold font-serif text-amber-100 mt-2">
                    The Grand Celestial Vault Query
                  </h3>
                  <p className="text-xs text-slate-400 font-sans mt-1">
                    "The library contains a collection of enchanted relics. Query the collection to claim the supreme Water key."
                  </p>
                </div>
                {player.conceptMastery.collections === 100 && (
                  <span className="px-3 py-1 rounded-full bg-emerald-950 border border-emerald-500/30 text-emerald-400 text-xs font-mono flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Solved
                  </span>
                )}
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-4">
                {/* Vault Items Table */}
                <div className="border border-slate-800 rounded-xl overflow-hidden text-xs font-mono">
                  <div className="bg-slate-900 px-4 py-2 text-slate-400 grid grid-cols-4 font-semibold">
                    <span>Artifact Name</span>
                    <span>Element</span>
                    <span>Power</span>
                    <span>Purity Status</span>
                  </div>
                  <div className="divide-y divide-slate-800 bg-slate-950">
                    {archiveVault.map(relic => (
                      <div key={relic.id} className="px-4 py-2.5 grid grid-cols-4 items-center">
                        <span className="text-amber-200 font-bold">{relic.name}</span>
                        <span className={relic.element === 'Water' ? 'text-sky-400' : 'text-slate-400'}>
                          {relic.element}
                        </span>
                        <span className="text-slate-300">{relic.power}</span>
                        <span className={relic.status === 'Pristine' ? 'text-emerald-400' : 'text-red-400'}>
                          {relic.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Query Controls */}
                <div className="grid md:grid-cols-3 gap-4 p-4 rounded-lg bg-slate-900 border border-slate-800">
                  <div className="space-y-1">
                    <span className="text-xs font-mono text-slate-400">Filter: Element Match</span>
                    <select
                      value={level6ElementFilter}
                      onChange={e => setLevel6ElementFilter(e.target.value as any)}
                      className="w-full bg-slate-950 border border-slate-700 rounded-lg p-2 text-xs font-mono text-amber-200"
                    >
                      <option value="All">All Elements</option>
                      <option value="Water">Water Only</option>
                      <option value="Fire">Fire Only</option>
                      <option value="Aether">Aether Only</option>
                    </select>
                  </div>

                  <div className="space-y-1">
                    <div className="flex justify-between text-xs font-mono text-slate-400">
                      <span>Filter: Minimum Power</span>
                      <span className="text-amber-300 font-bold">{level6MinPower}</span>
                    </div>
                    <input
                      type="range"
                      min="40"
                      max="95"
                      step="5"
                      value={level6MinPower}
                      onChange={e => setLevel6MinPower(parseInt(e.target.value))}
                      className="w-full accent-amber-500 cursor-pointer"
                    />
                  </div>

                  <div className="space-y-1 flex flex-col justify-end">
                    <button
                      onClick={() => setLevel6PristineOnly(!level6PristineOnly)}
                      className={`w-full py-2.5 rounded-lg text-xs font-mono font-bold transition flex items-center justify-center gap-2 ${
                        level6PristineOnly
                          ? 'bg-emerald-500 text-slate-950'
                          : 'bg-slate-800 text-slate-400'
                      }`}
                    >
                      {level6PristineOnly ? '✓ Pristine Only Enforced' : 'Allow Corrupted'}
                    </button>
                  </div>
                </div>

                <div className="pt-2 flex items-center justify-between border-t border-slate-800">
                  <div className="text-xs">
                    {level6Status === 'fail' && (
                      <span className="text-amber-400 font-sans flex items-center gap-1.5">
                        <AlertCircle className="w-4 h-4" /> {level6Message}
                      </span>
                    )}
                    {level6Status === 'success' && (
                      <span className="text-emerald-400 font-sans flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4" /> {level6Message}
                      </span>
                    )}
                  </div>
                  <button
                    onClick={runLevel6ArchiveQuery}
                    className="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-md shadow-amber-500/20 transition"
                  >
                    Execute Vault Collection Query &rarr;
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ---------------------------------------------------------------- */}
        {/* TAB 3: THE CODEX OF BECOMING */}
        {/* ---------------------------------------------------------------- */}
        {activeTab === 'codex' && (
          <div className="space-y-8">
            <div className="bg-slate-900/90 border border-amber-500/30 rounded-2xl p-6 md:p-8 shadow-xl">
              <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
                <span className="p-3 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/30">
                  <BookOpen className="w-6 h-6" />
                </span>
                <div>
                  <span className="text-xs font-mono text-amber-400 uppercase tracking-widest">
                    Living Learning Chronicle
                  </span>
                  <h2 className="text-2xl font-serif font-bold text-amber-100">
                    The Codex of Becoming
                  </h2>
                </div>
              </div>
              <p className="text-xs text-slate-400 mt-3 font-sans max-w-3xl">
                The Codex records your discoveries as fantasy achievements from gameplay rather than dry lessons.
                Review your Lore Discoveries, Masteries across the 6 computational primitives, and Your Scribed Craft.
              </p>
            </div>

            {/* Section 1: Discoveries */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-serif font-bold text-amber-200 flex items-center gap-2">
                  <Compass className="w-4 h-4 text-amber-400" /> Section I: Discoveries
                </h3>
                <span className="text-xs font-mono text-slate-400">{discoveries.length} Logged</span>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                {discoveries.map(item => (
                  <div
                    key={item.id}
                    className="p-5 rounded-2xl bg-slate-900 border border-slate-800 hover:border-amber-500/30 transition shadow-lg space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-bold font-serif text-amber-100">{item.title}</span>
                      <span className="text-[10px] font-mono text-amber-400 px-2 py-0.5 rounded bg-amber-500/10">
                        {item.location}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed font-sans">{item.lore}</p>
                    <div className="pt-2 text-[10px] font-mono text-slate-500 flex justify-end">
                      Inscribed: {item.dateUnlocked}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Section 2: Masteries */}
            <div className="space-y-4">
              <h3 className="text-lg font-serif font-bold text-amber-200 flex items-center gap-2">
                <Award className="w-4 h-4 text-amber-400" /> Section II: Masteries
              </h3>

              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {[
                  {
                    key: 'sequence',
                    title: 'Sequential Order',
                    primitive: 'ACTION',
                    score: player.conceptMastery.sequence,
                    desc: 'Ordering actions so instructions execute predictably from top to bottom.'
                  },
                  {
                    key: 'conditions',
                    title: 'Conditional Branching',
                    primitive: 'CONDITION',
                    score: player.conceptMastery.conditions,
                    desc: 'Allowing the realm to make decisions based on true or false states.'
                  },
                  {
                    key: 'loops',
                    title: 'Harmonic Repetition',
                    primitive: 'REPETITION',
                    score: player.conceptMastery.loops,
                    desc: 'Executing recurring incantations effortlessly over bounded cycles.'
                  },
                  {
                    key: 'variables',
                    title: 'Named Vessels',
                    primitive: 'VALUE',
                    score: player.conceptMastery.variables,
                    desc: 'Storing changing values under identifiable names in realm memory.'
                  },
                  {
                    key: 'functions',
                    title: 'Reusable Glyphs',
                    primitive: 'REUSABLE_ACTION',
                    score: player.conceptMastery.functions,
                    desc: 'Encapsulating complex rites into parameterized, reusable tools.'
                  },
                  {
                    key: 'collections',
                    title: 'Archival Sieves',
                    primitive: 'COLLECTION',
                    score: player.conceptMastery.collections,
                    desc: 'Querying, filtering, and organizing sets of items and relics.'
                  }
                ].map(m => (
                  <div
                    key={m.key}
                    className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-3 shadow-lg"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-amber-300">
                        {m.primitive}
                      </span>
                      <span className={`text-xs font-mono font-bold ${m.score === 100 ? 'text-emerald-400' : 'text-slate-500'}`}>
                        {m.score === 100 ? '✦ Mastered' : 'Locked'}
                      </span>
                    </div>
                    <div>
                      <h4 className="text-sm font-bold font-serif text-slate-100">{m.title}</h4>
                      <p className="text-xs text-slate-400 mt-1 font-sans">{m.desc}</p>
                    </div>
                    <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-amber-500 to-emerald-400 transition-all duration-500"
                        style={{ width: `${m.score}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Section 3: Your Craft */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-serif font-bold text-amber-200 flex items-center gap-2">
                  <Code2 className="w-4 h-4 text-amber-400" /> Section III: Your Craft
                </h3>
                <span className="text-xs font-mono text-slate-400">{scribedSpells.length} Formulas Scribed</span>
              </div>

              {scribedSpells.length === 0 ? (
                <div className="p-8 rounded-2xl bg-slate-900/60 border border-dashed border-slate-800 text-center space-y-2">
                  <Sparkles className="w-6 h-6 text-slate-600 mx-auto" />
                  <p className="text-sm text-slate-400 font-serif">No spells scribed yet.</p>
                  <p className="text-xs text-slate-500">
                    Complete the Trials in the Trials tab to unlock and record your craft here!
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {scribedSpells.map((spell, idx) => (
                    <div
                      key={idx}
                      className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4 shadow-lg"
                    >
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                        <div className="flex items-center gap-2">
                          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" />
                          <h4 className="font-serif font-bold text-amber-200 text-base">{spell.name}</h4>
                        </div>
                        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-950 border border-slate-800 text-amber-400 w-fit">
                          Primitive: {spell.primitive}
                        </span>
                      </div>

                      <div className="text-xs text-slate-300 italic font-serif">
                        &ldquo;{spell.fantasyIncantation}&rdquo;
                      </div>

                      <div className="grid md:grid-cols-2 gap-4 text-xs font-mono">
                        <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                          <span className="text-[10px] text-slate-500 uppercase block">Neutral Computational Primitive:</span>
                          <span className="text-amber-300 font-bold">{spell.universalLogic}</span>
                        </div>

                        <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                          <span className="text-[10px] text-slate-500 uppercase block">Real Code Expression (Python):</span>
                          <code className="text-emerald-300">{spell.pythonEquivalent}</code>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ---------------------------------------------------------------- */}
        {/* TAB 4: WORLD STATE & MAP */}
        {/* ---------------------------------------------------------------- */}
        {activeTab === 'world' && (
          <div className="space-y-6">
            <div className="bg-slate-900/90 border border-amber-500/30 rounded-2xl p-6 shadow-xl space-y-4">
              <h2 className="text-2xl font-serif font-bold text-amber-100 flex items-center gap-2">
                <Droplets className="w-6 h-6 text-sky-400" /> Realm of {world.kingdom} — Water Matrix Status
              </h2>
              <p className="text-xs text-slate-400 font-sans">
                Real-time hydrological and spiritual state of the kingdom. As you overcome computational trials,
                the water network revives and morale surges across the townsfolk.
              </p>

              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                  <span className="text-[10px] font-mono text-slate-500 uppercase">Mountain Spring Flow</span>
                  <div className="text-lg font-bold font-serif text-sky-300 capitalize">{world.waterSupply}</div>
                  <div className="text-[11px] text-slate-400">
                    {world.waterSupply === 'restored' ? 'Full cascading torrent' : 'Dry stone canals'}
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                  <span className="text-[10px] font-mono text-slate-500 uppercase">Clockwork Sentinel</span>
                  <div className="text-lg font-bold font-serif text-amber-300 capitalize">{world.guardianStatus}</div>
                  <div className="text-[11px] text-slate-400">
                    {world.guardianStatus === 'operational' ? 'Clutch gear engaged' : 'Dormant on dais'}
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                  <span className="text-[10px] font-mono text-slate-500 uppercase">Grove Spirit Trust</span>
                  <div className="text-lg font-bold font-serif text-emerald-300">{world.spiritTrust} / 10</div>
                  <div className="text-[11px] text-slate-400">
                    {world.spiritTrust > 0 ? 'Sacred conditions verified' : 'Portal warded'}
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                  <span className="text-[10px] font-mono text-slate-500 uppercase">Celestial Archive</span>
                  <div className="text-lg font-bold font-serif text-purple-300 capitalize">{world.archiveStatus}</div>
                  <div className="text-[11px] text-slate-400">
                    {world.archiveStatus === 'opened' ? 'Master valve unlocked' : 'Locked by riddle'}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ---------------------------------------------------------------- */}
        {/* TAB 5: AUTONOMOUS AGENTS TELEMETRY */}
        {/* ---------------------------------------------------------------- */}
        {activeTab === 'agents' && (
          <div className="space-y-6">
            <div className="bg-slate-900/90 border border-amber-500/30 rounded-2xl p-6 shadow-xl space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-serif font-bold text-amber-100 flex items-center gap-2">
                    <Cpu className="w-6 h-6 text-purple-400" /> Multi-Agent Orchestration Telemetry
                  </h2>
                  <p className="text-xs text-slate-400 font-sans mt-1">
                    Live logs from the six coordinating agents powering narrative coherence, deterministic pedagogical validation, and world laws.
                  </p>
                </div>
                <span className="px-3 py-1 rounded-full bg-emerald-950 border border-emerald-500/30 text-emerald-400 font-mono text-xs">
                  6 Agents Operational
                </span>
              </div>

              <div className="grid md:grid-cols-3 gap-3 text-xs font-mono pt-2">
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                  <span className="text-amber-400 font-bold block">DirectorAgent</span>
                  <span className="text-slate-400">Narrative arc & user intent coordinator</span>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                  <span className="text-emerald-400 font-bold block">LogicLearningAgent</span>
                  <span className="text-slate-400">Deterministic code & concept validator</span>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                  <span className="text-sky-400 font-bold block">WorldKeeperAgent</span>
                  <span className="text-slate-400">Invariants, geography & resource continuity</span>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                  <span className="text-purple-400 font-bold block">PlayerInsightAgent</span>
                  <span className="text-slate-400">Adaptive profiling & difficulty scaling</span>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                  <span className="text-pink-400 font-bold block">StoryWeaverAgent</span>
                  <span className="text-slate-400">Atmospheric prose & NPC dialogue generation</span>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                  <span className="text-indigo-400 font-bold block">ContinuitySafetyAgent</span>
                  <span className="text-slate-400">Content moderation & invariant safety gate</span>
                </div>
              </div>

              <div className="pt-4 border-t border-slate-800">
                <span className="text-xs font-mono text-slate-400 uppercase tracking-wider block mb-3">
                  Telemetry Event Stream:
                </span>
                <div className="space-y-2 font-mono text-xs max-h-80 overflow-y-auto pr-2">
                  {telemetry.map((t, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-start gap-3">
                      <span className="text-amber-400 font-bold min-w-36">{t.agent}:</span>
                      <span className="text-slate-300 flex-1">{t.output}</span>
                      <span className="text-[10px] text-emerald-400 uppercase px-2 py-0.5 rounded bg-emerald-950 border border-emerald-500/20">
                        {t.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-950 px-4 py-4 text-center text-xs text-slate-500 font-sans">
        MythCode &copy; 2026 • Experiential Programming & Fantasy Adventure • Powered by Multi-Agent Architecture
      </footer>
    </div>
  );
}
