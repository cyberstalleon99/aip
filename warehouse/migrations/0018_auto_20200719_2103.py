# Generated by Django 2.1.1 on 2020-07-19 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0017_auto_20200622_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outgoing',
            name='item_work',
            field=models.CharField(choices=[('N/A', 'N/A'), ('Active Protection System', 'Active Protection System'), ('Active Wire Mesh System (High Tensile)', 'Active Wire Mesh System (High Tensile)'), ('Aggregate Subbase Course', 'Aggregate Subbase Course'), ('Chevron Signs (450mm X 600mm)', 'Chevron Signs (450mm X 600mm)'), ('Concrete (Slope Protection)', 'Concrete (Slope Protection)'), ('Concrete Curb (Cast in Place)', 'Concrete Curb (Cast in Place)'), ('Concrete Gutter, Cast in Place', 'Concrete Gutter, Cast in Place'), ('Concrete Railing (Standard)', 'Concrete Railing (Standard)'), ('Curb and gutter, cast-in-place', 'Curb and gutter, cast-in-place'), ('Danger/Warning Signs (60 cm Triangle) W1-3', 'Danger/Warning Signs (60 cm Triangle) W1-3'), ('Detour/ Access Road', 'Detour/ Access Road'), ('Drain Pipe (Galvanized)', 'Drain Pipe (Galvanized)'), ('Drain Pipe (PVC)', 'Drain Pipe (PVC)'), ('Elastomeric Bearing Pad', 'Elastomeric Bearing Pad'), ('Erosion Control Mat (Type 4)', 'Erosion Control Mat (Type 4)'), ('Erosion Control Mat (Type I)', 'Erosion Control Mat (Type I)'), ('Expansion Joint (Rubber Multiplex)', 'Expansion Joint (Rubber Multiplex)'), ('Filter Cloth', 'Filter Cloth'), ('Forms and Falsework', 'Forms and Falsework'), ('Gabions (1mx1mx2m, Metallic Coated)', 'Gabions (1mx1mx2m, Metallic Coated)'), ('Grouted Riprap (Class A)', 'Grouted Riprap (Class A)'), ('Hand-Laid Rock Embankment', 'Hand-Laid Rock Embankment'), ('Hazard Markers (600 x 800mm)', 'Hazard Markers (600 x 800mm)'), ('Hazard Markers (Chevron Signs, 450x600mm)', 'Hazard Markers (Chevron Signs, 450x600mm)'), ('Hydroseeding', 'Hydroseeding'), ('Individual Removal of Trees (Small, 150mm - 300mm dia.)', 'Individual Removal of Trees (Small, 150mm - 300mm dia.)'), ('Individual Removal of Trees (Small, 301mm - 500mm dia.)', 'Individual Removal of Trees (Small, 301mm - 500mm dia.)'), ('Individual Removal of Trees, 501-750 mm dia', 'Individual Removal of Trees, 501-750 mm dia'), ('Inlet Type (910 mm dia.)', 'Inlet Type (910 mm dia.)'), ('Lean Concrete (class B, 16.50Mpa)', 'Lean Concrete (class B, 16.50Mpa)'), ('Metal beam end piece', 'Metal beam end piece'), ('Metal Guardrails (Metal Beam) including Concrete Post', 'Metal Guardrails (Metal Beam) including Concrete Post'), ('Occupational Safety and Health Program', 'Occupational Safety and Health Program'), ('Paint', 'Paint'), ('Passive System, Hybrid Drapery', 'Passive System, Hybrid Drapery'), ('PCCP  (Unreinforced 0.15 m thick, 14 Days)', 'PCCP  (Unreinforced 0.15 m thick, 14 Days)'), ('PCCP  (Unreinforced 0.23 m thick - 14 Days)', 'PCCP  (Unreinforced 0.23 m thick - 14 Days)'), ('PCCP (Unreinforced 0.28 m thick, 14 Days)', 'PCCP (Unreinforced 0.28 m thick, 14 Days)'), ('Permanent Ground Anchor', 'Permanent Ground Anchor'), ('Pipe Culvert (910 mm Dia., Class II)', 'Pipe Culvert (910 mm Dia., Class II)'), ('Pipe Culverts (910mm dia. Class II - RCPC)', 'Pipe Culverts (910mm dia. Class II - RCPC)'), ('Pipe Culverts 610mm diameter (24”ɸ) class II RCPC (V.O.)new item', 'Pipe Culverts 610mm diameter (24”ɸ) class II RCPC (V.O.)new item'), ('Preformed Sponge Rubber Joint Expansion', 'Preformed Sponge Rubber Joint Expansion'), ('Premolded Expansion Joint Filler with Sealant', 'Premolded Expansion Joint Filler with Sealant'), ('Project Billboard/ Signboard (For COA)', 'Project Billboard/ Signboard (For COA)'), ('Project Billboard/ Signboard (For DPWH)', 'Project Billboard/ Signboard (For DPWH)'), ('Reflectorized Pavement Studs Raised Profile Type (Bi - Directional)', 'Reflectorized Pavement Studs Raised Profile Type (Bi - Directional)'), ('Reflectorized Thermoplastic Pavement Markings White', 'Reflectorized Thermoplastic Pavement Markings White'), ('Regulatory Signs (600mm Ø, R6-4, Miscellaneous Signs, Load and Dimension Restriction Signs)', 'Regulatory Signs (600mm Ø, R6-4, Miscellaneous Signs, Load and Dimension Restriction Signs)'), ('Reinforcing Steel (Grade 40)', 'Reinforcing Steel (Grade 40)'), ('Reinforcing Steel (Grade 60)', 'Reinforcing Steel (Grade 60)'), ('Reinforcing Steel (Headwalls, Catch basins)', 'Reinforcing Steel (Headwalls, Catch basins)'), ('Relocation of Utilities (3 pcs. Electrical Post)', 'Relocation of Utilities (3 pcs. Electrical Post)'), ('Right-of-Way Monument (Precast Concrete)', 'Right-of-Way Monument (Precast Concrete)'), ('Rockfall Netting', 'Rockfall Netting'), ('Shotcrete with Reinforcing Fiber', 'Shotcrete with Reinforcing Fiber'), ('Solar LED Street Light', 'Solar LED Street Light'), ('Steel Sheet Pile (Slope Protection)', 'Steel Sheet Pile (Slope Protection)'), ('Stone masonry', 'Stone masonry'), ('Structural Concrete (Class "A" - 20.68Mpa, 28 days)', 'Structural Concrete (Class "A" - 20.68Mpa, 28 days)'), ('Structural Concrete (Class "A" - 27.56Mpa, 28 days)', 'Structural Concrete (Class "A" - 27.56Mpa, 28 days)'), ('Structural Concrete (Class "B" - 16.50Mpa, 28 days)', 'Structural Concrete (Class "B" - 16.50Mpa, 28 days)'), ('Structural Concrete (Headwalls, Catch basins)', 'Structural Concrete (Headwalls, Catch basins)'), ('Structural Concrete (Painting Works)', 'Structural Concrete (Painting Works)'), ('Structural concrete class A (minor Structure)', 'Structural concrete class A (minor Structure)'), ('Structural Concrete, Class A (Catch Basin, Headwall, RCBC)', 'Structural Concrete, Class A (Catch Basin, Headwall, RCBC)'), ('Structural concrete, class A(minor structures)', 'Structural concrete, class A(minor structures)'), ('Structural Steel, Furnished, Fabricated, and Erected (Grade 36)', 'Structural Steel, Furnished, Fabricated, and Erected (Grade 36)'), ('Warning Signs', 'Warning Signs'), ('Welded Structural Steel (Waiting Shed)', 'Welded Structural Steel (Waiting Shed)')], default='N/A', max_length=200, verbose_name='Work Item'),
        ),
    ]
