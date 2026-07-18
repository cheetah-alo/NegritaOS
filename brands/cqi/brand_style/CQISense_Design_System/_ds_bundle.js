/* @ds-bundle: {"format":4,"namespace":"CQISenseDesignSystem_73301e","components":[{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"CardHeader","sourcePath":"components/core/Card.jsx"},{"name":"Stat","sourcePath":"components/core/Stat.jsx"},{"name":"ARCHETYPES","sourcePath":"components/domain/ArchetypeBadge.jsx"},{"name":"ArchetypeBadge","sourcePath":"components/domain/ArchetypeBadge.jsx"},{"name":"MECHANISMS","sourcePath":"components/domain/MechanismTag.jsx"},{"name":"MechanismTag","sourcePath":"components/domain/MechanismTag.jsx"},{"name":"PointsPill","sourcePath":"components/domain/PointsPill.jsx"},{"name":"ChannelSplit","sourcePath":"components/domain/PointsPill.jsx"},{"name":"RuleCard","sourcePath":"components/domain/RuleCard.jsx"},{"name":"ScoreMeter","sourcePath":"components/domain/ScoreMeter.jsx"}],"sourceHashes":{"components/core/Badge.jsx":"ff28200b7ee8","components/core/Button.jsx":"535f30688d5c","components/core/Card.jsx":"94dae65b8452","components/core/Stat.jsx":"aaf3778d7ffc","components/domain/ArchetypeBadge.jsx":"398983c949c7","components/domain/MechanismTag.jsx":"2d9fca7fa3db","components/domain/PointsPill.jsx":"be1726cd7135","components/domain/RuleCard.jsx":"288968360b3e","components/domain/ScoreMeter.jsx":"7439459fa6c3"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.CQISenseDesignSystem_73301e = window.CQISenseDesignSystem_73301e || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Badge — small status/label chip. Soft (tinted) or solid fill.
 * tone: neutral | brand | repair | risk | success | warning | danger | info | heat
 */
const TONES = {
  neutral: {
    soft: ['var(--gray-100)', 'var(--text-body)'],
    solid: ['var(--gray-700)', 'var(--text-inverse)']
  },
  brand: {
    soft: ['var(--brand-soft)', 'var(--brand-hover)'],
    solid: ['var(--brand)', 'var(--on-brand)']
  },
  repair: {
    soft: ['var(--repair-soft)', 'var(--repair-text)'],
    solid: ['var(--repair)', 'var(--white)']
  },
  risk: {
    soft: ['var(--risk-soft)', 'var(--risk-text)'],
    solid: ['var(--risk)', 'var(--white)']
  },
  success: {
    soft: ['var(--success-soft)', 'var(--success-text)'],
    solid: ['var(--success)', 'var(--white)']
  },
  warning: {
    soft: ['var(--warning-soft)', 'var(--warning-text)'],
    solid: ['var(--warning)', 'var(--white)']
  },
  danger: {
    soft: ['var(--danger-soft)', 'var(--danger-text)'],
    solid: ['var(--danger)', 'var(--white)']
  },
  info: {
    soft: ['var(--info-soft)', 'var(--info-text)'],
    solid: ['var(--info)', 'var(--white)']
  },
  heat: {
    soft: ['var(--heat-soft)', 'var(--heat-text)'],
    solid: ['var(--heat)', 'var(--white)']
  }
};
function Badge({
  children,
  tone = 'neutral',
  solid = false,
  dot = false,
  mono = false,
  style = {},
  ...rest
}) {
  const [bg, fg] = TONES[tone] ? TONES[tone][solid ? 'solid' : 'soft'] : TONES.neutral.soft;
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '6px',
      padding: '3px 9px',
      borderRadius: 'var(--radius-full)',
      background: bg,
      color: fg,
      fontFamily: mono ? 'var(--font-mono)' : 'var(--font-body)',
      fontSize: 'var(--text-xs)',
      fontWeight: 'var(--weight-semibold)',
      letterSpacing: mono ? '0.02em' : '0.01em',
      lineHeight: 1.4,
      whiteSpace: 'nowrap',
      ...style
    }
  }, rest), dot && /*#__PURE__*/React.createElement("span", {
    style: {
      width: 6,
      height: 6,
      borderRadius: '50%',
      background: fg,
      opacity: 0.8
    }
  }), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * CQISense Button — bold, confident, cobalt-first.
 * Variants: primary (cobalt fill), secondary (outline), ghost, danger.
 * Sizes: sm | md | lg.
 */
function Button({
  children,
  variant = 'primary',
  size = 'md',
  iconLeft = null,
  iconRight = null,
  disabled = false,
  full = false,
  style = {},
  ...rest
}) {
  const sizes = {
    sm: {
      height: 'var(--control-sm)',
      padding: '0 12px',
      font: 'var(--text-sm)',
      radius: 'var(--radius-sm)',
      gap: '6px'
    },
    md: {
      height: 'var(--control-md)',
      padding: '0 16px',
      font: 'var(--text-sm)',
      radius: 'var(--radius-md)',
      gap: '8px'
    },
    lg: {
      height: 'var(--control-lg)',
      padding: '0 22px',
      font: 'var(--text-md)',
      radius: 'var(--radius-md)',
      gap: '9px'
    }
  }[size];
  const variants = {
    primary: {
      background: 'var(--brand)',
      color: 'var(--on-brand)',
      border: '1px solid var(--brand)'
    },
    secondary: {
      background: 'var(--surface-card)',
      color: 'var(--text-strong)',
      border: '1px solid var(--border-strong)'
    },
    ghost: {
      background: 'transparent',
      color: 'var(--text-body)',
      border: '1px solid transparent'
    },
    danger: {
      background: 'var(--danger)',
      color: 'var(--text-inverse)',
      border: '1px solid var(--danger)'
    }
  }[variant];
  const [hover, setHover] = React.useState(false);
  const hoverBg = {
    primary: 'var(--brand-hover)',
    secondary: 'var(--gray-100)',
    ghost: 'var(--gray-100)',
    danger: 'var(--pink-500)'
  }[variant];
  return /*#__PURE__*/React.createElement("button", _extends({
    disabled: disabled,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: sizes.gap,
      height: sizes.height,
      padding: sizes.padding,
      width: full ? '100%' : 'auto',
      fontFamily: 'var(--font-body)',
      fontSize: sizes.font,
      fontWeight: 'var(--weight-semibold)',
      letterSpacing: '0.01em',
      lineHeight: 1,
      whiteSpace: 'nowrap',
      borderRadius: sizes.radius,
      cursor: disabled ? 'not-allowed' : 'pointer',
      transition: 'background var(--dur-fast) var(--ease-out), transform var(--dur-fast) var(--ease-out)',
      opacity: disabled ? 0.45 : 1,
      transform: hover && !disabled ? 'translateY(-1px)' : 'none',
      ...variants,
      ...(hover && !disabled ? {
        background: hoverBg,
        borderColor: hoverBg
      } : null),
      ...(variant === 'secondary' && hover && !disabled ? {
        borderColor: 'var(--border-strong)',
        background: 'var(--gray-100)'
      } : null),
      ...style
    }
  }, rest), iconLeft, children, iconRight);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Card — the base surface. Paper-flat by default (hairline border),
 * optional soft elevation, optional accent rail on the left edge.
 */
function Card({
  children,
  elevation = 'flat',
  // 'flat' | 'raised' | 'floating'
  accent = null,
  // CSS color for a 3px left rail (e.g. 'var(--repair)')
  pad = 'md',
  // 'none' | 'sm' | 'md' | 'lg'
  style = {},
  ...rest
}) {
  const shadow = {
    flat: 'none',
    raised: 'var(--shadow-sm)',
    floating: 'var(--shadow-lg)'
  }[elevation];
  const padding = {
    none: 0,
    sm: '14px',
    md: '20px',
    lg: '28px'
  }[pad];
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      position: 'relative',
      background: 'var(--surface-card)',
      border: '1px solid var(--border-hair)',
      borderRadius: 'var(--radius-md)',
      boxShadow: shadow,
      padding,
      overflow: 'hidden',
      ...style
    }
  }, rest), accent && /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      left: 0,
      top: 0,
      bottom: 0,
      width: 3,
      background: accent,
      borderRadius: '3px 0 0 3px'
    }
  }), children);
}

/** Optional card header: eyebrow + title + right-aligned actions. */
function CardHeader({
  eyebrow,
  title,
  actions = null,
  style = {}
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      justifyContent: 'space-between',
      gap: 16,
      marginBottom: 16,
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", null, eyebrow && /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-xs)',
      fontWeight: 500,
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-caps)',
      color: 'var(--text-muted)',
      marginBottom: 5
    }
  }, eyebrow), title && /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-xl)',
      fontWeight: 600,
      color: 'var(--text-strong)',
      letterSpacing: 'var(--tracking-snug)'
    }
  }, title)), actions);
}
Object.assign(__ds_scope, { Card, CardHeader });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/Stat.jsx
try { (() => {
/**
 * Stat — a single metric: label, big mono value, optional unit + delta.
 * The workhorse for ADHD-friendly slides: one number, stated plainly.
 */
function Stat({
  label,
  value,
  unit = null,
  delta = null,
  // e.g. "+1.8%" or "-9ms"
  direction = null,
  // 'up' | 'down' | null  (semantic, not arrow direction)
  goodWhen = 'up',
  // 'up' | 'down' — which direction is "good" (green)
  size = 'md',
  // 'sm' | 'md' | 'lg' | 'xl'
  hint = null,
  style = {}
}) {
  const valSize = {
    sm: 'var(--text-xl)',
    md: 'var(--text-2xl)',
    lg: 'var(--text-4xl)',
    xl: 'var(--text-5xl)'
  }[size];
  const good = direction === goodWhen;
  const deltaColor = direction == null ? 'var(--text-muted)' : good ? 'var(--pos)' : 'var(--neg)';
  const arrow = direction === 'up' ? '▲' : direction === 'down' ? '▼' : '';
  return /*#__PURE__*/React.createElement("div", {
    style: style
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--text-sm)',
      color: 'var(--text-muted)',
      letterSpacing: '0.01em',
      marginBottom: 8
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontWeight: 500,
      color: 'var(--text-strong)',
      fontSize: valSize,
      lineHeight: 1,
      letterSpacing: '-0.01em',
      fontVariantNumeric: 'tabular-nums'
    }
  }, value), unit && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-md)',
      color: 'var(--text-muted)'
    }
  }, unit), delta != null && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-sm)',
      fontWeight: 600,
      color: deltaColor,
      fontVariantNumeric: 'tabular-nums',
      display: 'inline-flex',
      alignItems: 'center',
      gap: 3
    }
  }, arrow && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: '0.8em'
    }
  }, arrow), delta)), hint && /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 'var(--text-xs)',
      color: 'var(--text-subtle)',
      marginTop: 6
    }
  }, hint));
}
Object.assign(__ds_scope, { Stat });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Stat.jsx", error: String((e && e.message) || e) }); }

// components/domain/ArchetypeBadge.jsx
try { (() => {
/**
 * ArchetypeBadge — the journey-state archetypes (A, B, C, D, D2, E, F).
 * Renders a colored letter token + optional full name. The archetype is
 * always the FINAL, prioritized label for a journey.
 */
const ARCHETYPES = {
  A: {
    name: 'Resolved Low Pressure',
    color: 'var(--arch-a)'
  },
  B: {
    name: 'Operational Loop',
    color: 'var(--arch-b)'
  },
  C: {
    name: 'Repair Failure / Recall Risk',
    color: 'var(--arch-c)'
  },
  D: {
    name: 'Exit Risk Proximity',
    color: 'var(--arch-d)'
  },
  D2: {
    name: 'Broken Promise + Exit',
    color: 'var(--arch-d2)'
  },
  E: {
    name: 'Silent Failure / Gap',
    color: 'var(--arch-e)'
  },
  F: {
    name: 'Uncertain Review',
    color: 'var(--arch-f)'
  }
};
function ArchetypeBadge({
  code = 'C',
  showName = true,
  size = 'md',
  style = {}
}) {
  const a = ARCHETYPES[code] || ARCHETYPES.C;
  const dim = {
    sm: 22,
    md: 28,
    lg: 38
  }[size];
  const fz = {
    sm: 'var(--text-xs)',
    md: 'var(--text-sm)',
    lg: 'var(--text-lg)'
  }[size];
  const nameFz = {
    sm: 'var(--text-xs)',
    md: 'var(--text-sm)',
    lg: 'var(--text-md)'
  }[size];
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 10,
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: dim,
      height: dim,
      minWidth: dim,
      borderRadius: 'var(--radius-sm)',
      background: a.color,
      color: 'var(--white)',
      display: 'grid',
      placeItems: 'center',
      fontFamily: 'var(--font-display)',
      fontWeight: 600,
      fontSize: fz,
      letterSpacing: '-0.01em',
      boxShadow: 'var(--shadow-xs)'
    }
  }, code), showName && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-body)',
      fontSize: nameFz,
      fontWeight: 600,
      color: 'var(--text-strong)',
      lineHeight: 1.2
    }
  }, a.name));
}
Object.assign(__ds_scope, { ARCHETYPES, ArchetypeBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/domain/ArchetypeBadge.jsx", error: String((e && e.message) || e) }); }

// components/domain/MechanismTag.jsx
try { (() => {
/**
 * MechanismTag — the "why" behind a journey (mechanisms can be multiple).
 * Rendered as a quiet outlined tag with a family dot (repair / risk / mixed).
 */
const MECHANISMS = {
  PROMISE_DEBT_TO_FRICTION: {
    label: 'Promise Debt → Friction',
    family: 'repair'
  },
  TECHNICAL_REPAIR_FAILURE: {
    label: 'Technical Repair Failure',
    family: 'repair'
  },
  OPERATIONAL_LOOP: {
    label: 'Operational Loop',
    family: 'repair'
  },
  FRICTION_REPAIR_GAP: {
    label: 'Friction Repair Gap',
    family: 'repair'
  },
  UNRESOLVED_MULTI_CALL_FATIGUE: {
    label: 'Unresolved Multi-Call Fatigue',
    family: 'repair'
  },
  COMPETITIVE_EXIT_PRESSURE: {
    label: 'Competitive Exit Pressure',
    family: 'risk'
  },
  BROKEN_PROMISE_EXIT_ESCALATION: {
    label: 'Broken Promise + Exit Escalation',
    family: 'mixed'
  },
  RESOLVED_LOW_PRESSURE: {
    label: 'Resolved Low Pressure',
    family: 'relief'
  }
};
const FAMILY_COLOR = {
  repair: 'var(--repair)',
  risk: 'var(--risk)',
  mixed: 'var(--arch-d2)',
  relief: 'var(--relief)'
};
function MechanismTag({
  id,
  label,
  family,
  size = 'md',
  style = {}
}) {
  const m = id && MECHANISMS[id] ? MECHANISMS[id] : null;
  const text = label ?? (m ? m.label : id);
  const fam = family ?? (m ? m.family : 'repair');
  const color = FAMILY_COLOR[fam] || 'var(--repair)';
  const pad = size === 'sm' ? '4px 9px' : '5px 11px';
  const fz = size === 'sm' ? 'var(--text-xs)' : 'var(--text-sm)';
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 7,
      padding: pad,
      border: '1px solid var(--border-soft)',
      borderRadius: 'var(--radius-full)',
      background: 'var(--surface-card)',
      color: 'var(--text-body)',
      fontFamily: 'var(--font-body)',
      fontSize: fz,
      fontWeight: 500,
      whiteSpace: 'nowrap',
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 8,
      height: 8,
      borderRadius: '50%',
      background: color
    }
  }), text);
}
Object.assign(__ds_scope, { MECHANISMS, MechanismTag });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/domain/MechanismTag.jsx", error: String((e && e.message) || e) }); }

// components/domain/PointsPill.jsx
try { (() => {
/**
 * PointsPill — a scoring contribution like "+25" or a channel split
 * "TSR +8 / CSR +10". Colored by score family (repair / risk / neutral).
 */
function PointsPill({
  value,
  family = 'repair',
  size = 'md',
  style = {}
}) {
  const palette = {
    repair: ['var(--repair-soft)', 'var(--repair-text)'],
    risk: ['var(--risk-soft)', 'var(--risk-text)'],
    neutral: ['var(--gray-100)', 'var(--gray-700)'],
    relief: ['var(--green-100)', 'var(--green-800)']
  }[family] || ['var(--repair-soft)', 'var(--repair-text)'];
  const fz = size === 'sm' ? 'var(--text-xs)' : size === 'lg' ? 'var(--text-md)' : 'var(--text-sm)';
  const pad = size === 'sm' ? '2px 8px' : '3px 10px';
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      padding: pad,
      borderRadius: 'var(--radius-sm)',
      background: palette[0],
      color: palette[1],
      fontFamily: 'var(--font-mono)',
      fontSize: fz,
      fontWeight: 600,
      fontVariantNumeric: 'tabular-nums',
      whiteSpace: 'nowrap',
      letterSpacing: '0.01em',
      ...style
    }
  }, value);
}

/** ChannelSplit — TSR vs CSR point split, the canonical rule weighting display. */
function ChannelSplit({
  tsr,
  csr,
  family = 'repair',
  style = {}
}) {
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-xs)',
      color: 'var(--text-muted)'
    }
  }, "TSR"), /*#__PURE__*/React.createElement(PointsPill, {
    value: tsr,
    family: family,
    size: "sm"
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--border-strong)'
    }
  }, "/"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-xs)',
      color: 'var(--text-muted)'
    }
  }, "CSR"), /*#__PURE__*/React.createElement(PointsPill, {
    value: csr,
    family: family,
    size: "sm"
  }));
}
Object.assign(__ds_scope, { PointsPill, ChannelSplit });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/domain/PointsPill.jsx", error: String((e && e.message) || e) }); }

// components/domain/RuleCard.jsx
try { (() => {
/**
 * RuleCard — the "one-row contract" for an Attr Strict rule (R1..R9):
 * code, title, score family, channel points, mechanism, archetype, support.
 * Composes core + domain primitives.
 */
function RuleCard({
  code,
  // 'R1'
  title,
  // 'Callback Promise Debt'
  family = 'repair',
  // 'repair' | 'risk' | 'priority'
  tsr,
  csr,
  // points per channel
  mechanism,
  // mechanism id
  archetype,
  // archetype code
  strictCalls = null,
  // e.g. '87,626'
  strictShare = null,
  // e.g. '62.5%'
  status = 'Proposal',
  // rule status
  style = {}
}) {
  const famTone = family === 'risk' ? 'risk' : family === 'priority' ? 'heat' : 'repair';
  const accent = family === 'risk' ? 'var(--risk)' : family === 'priority' ? 'var(--heat)' : 'var(--repair)';
  return /*#__PURE__*/React.createElement(__ds_scope.Card, {
    accent: accent,
    pad: "md",
    style: style
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontWeight: 600,
      fontSize: 'var(--text-sm)',
      color: 'var(--text-muted)'
    }
  }, code), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--text-lg)',
      fontWeight: 600,
      color: 'var(--text-strong)',
      flex: 1,
      lineHeight: 1.2
    }
  }, title), /*#__PURE__*/React.createElement(__ds_scope.Badge, {
    tone: famTone,
    solid: true
  }, family === 'priority' ? 'Priority route' : family[0].toUpperCase() + family.slice(1))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '14px 20px'
    }
  }, /*#__PURE__*/React.createElement(Field, {
    label: "Points"
  }, tsr != null ? /*#__PURE__*/React.createElement(__ds_scope.ChannelSplit, {
    tsr: tsr,
    csr: csr,
    family: famTone
  }) : /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-sm)',
      color: 'var(--text-muted)'
    }
  }, "0 standalone")), /*#__PURE__*/React.createElement(Field, {
    label: "Archetype"
  }, /*#__PURE__*/React.createElement(__ds_scope.ArchetypeBadge, {
    code: archetype,
    size: "sm"
  })), /*#__PURE__*/React.createElement(Field, {
    label: "Mechanism"
  }, /*#__PURE__*/React.createElement(__ds_scope.MechanismTag, {
    id: mechanism,
    size: "sm"
  })), /*#__PURE__*/React.createElement(Field, {
    label: "Status"
  }, /*#__PURE__*/React.createElement(__ds_scope.Badge, {
    tone: "neutral"
  }, status))), (strictCalls || strictShare) && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 24,
      marginTop: 16,
      paddingTop: 14,
      borderTop: '1px solid var(--border-hair)'
    }
  }, strictCalls && /*#__PURE__*/React.createElement(Mini, {
    label: "Strict calls",
    value: strictCalls
  }), strictShare && /*#__PURE__*/React.createElement(Mini, {
    label: "Strict share",
    value: strictShare
  })));
}
function Field({
  label,
  children
}) {
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-2xs)',
      textTransform: 'uppercase',
      letterSpacing: 'var(--tracking-caps)',
      color: 'var(--text-subtle)',
      marginBottom: 6
    }
  }, label), children);
}
function Mini({
  label,
  value
}) {
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontWeight: 500,
      fontSize: 'var(--text-md)',
      color: 'var(--text-strong)',
      fontVariantNumeric: 'tabular-nums'
    }
  }, value), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-xs)',
      color: 'var(--text-muted)',
      marginLeft: 6
    }
  }, label));
}
Object.assign(__ds_scope, { RuleCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/domain/RuleCard.jsx", error: String((e && e.message) || e) }); }

// components/domain/ScoreMeter.jsx
try { (() => {
/**
 * ScoreMeter — a 0-100 pressure score (Repair / Risk / Operational) shown as
 * a calm horizontal meter with a big mono value. Optional threshold marker
 * (e.g. the >=55 archetype-promotion line).
 */
const FAMILY = {
  repair: {
    track: 'var(--repair-soft)',
    fill: 'var(--repair)',
    text: 'var(--repair-text)',
    label: 'Repair Pressure'
  },
  risk: {
    track: 'var(--risk-soft)',
    fill: 'var(--risk)',
    text: 'var(--risk-text)',
    label: 'Risk Pressure'
  },
  operational: {
    track: 'var(--operational-soft)',
    fill: 'var(--operational)',
    text: 'var(--green-800)',
    label: 'Operational Score'
  }
};
function ScoreMeter({
  value,
  // 0..100
  family = 'operational',
  label = null,
  // overrides default family label
  threshold = null,
  // 0..100 marker line, e.g. 55
  thresholdLabel = null,
  max = 100,
  size = 'md',
  // 'sm' | 'md' | 'lg'
  style = {}
}) {
  const f = FAMILY[family] || FAMILY.operational;
  const pct = Math.max(0, Math.min(100, value / max * 100));
  const h = {
    sm: 8,
    md: 12,
    lg: 16
  }[size];
  const valFz = {
    sm: 'var(--text-xl)',
    md: 'var(--text-2xl)',
    lg: 'var(--text-4xl)'
  }[size];
  return /*#__PURE__*/React.createElement("div", {
    style: style
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      justifyContent: 'space-between',
      marginBottom: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 'var(--text-sm)',
      fontWeight: 600,
      color: 'var(--text-muted)',
      letterSpacing: '0.01em'
    }
  }, label ?? f.label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontWeight: 500,
      fontSize: valFz,
      color: f.text,
      lineHeight: 1,
      fontVariantNumeric: 'tabular-nums'
    }
  }, value, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: '0.5em',
      color: 'var(--text-subtle)',
      marginLeft: 2
    }
  }, "/", max))), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      height: h,
      borderRadius: 'var(--radius-full)',
      background: f.track,
      overflow: 'visible'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: 0,
      top: 0,
      bottom: 0,
      width: pct + '%',
      background: f.fill,
      borderRadius: 'var(--radius-full)',
      transition: 'width var(--dur-slow) var(--ease-out)'
    }
  }), threshold != null && /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      left: threshold / max * 100 + '%',
      top: -3,
      bottom: -3,
      width: 2,
      background: 'var(--gray-700)',
      borderRadius: 2
    }
  }, thresholdLabel && /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      top: -18,
      left: '50%',
      transform: 'translateX(-50%)',
      whiteSpace: 'nowrap',
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--text-2xs)',
      color: 'var(--gray-700)'
    }
  }, thresholdLabel))));
}
Object.assign(__ds_scope, { ScoreMeter });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/domain/ScoreMeter.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.CardHeader = __ds_scope.CardHeader;

__ds_ns.Stat = __ds_scope.Stat;

__ds_ns.ARCHETYPES = __ds_scope.ARCHETYPES;

__ds_ns.ArchetypeBadge = __ds_scope.ArchetypeBadge;

__ds_ns.MECHANISMS = __ds_scope.MECHANISMS;

__ds_ns.MechanismTag = __ds_scope.MechanismTag;

__ds_ns.PointsPill = __ds_scope.PointsPill;

__ds_ns.ChannelSplit = __ds_scope.ChannelSplit;

__ds_ns.RuleCard = __ds_scope.RuleCard;

__ds_ns.ScoreMeter = __ds_scope.ScoreMeter;

})();
