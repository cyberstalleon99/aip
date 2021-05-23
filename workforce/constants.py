UNIT_TYPE = (
    ('Uncategorized','Uncategorized'),
    ('BD', 'BD'),
    ('CC', 'CC'),
    ('CCT', 'CCT'),
    ('CP', 'CP'),
    ('CT', 'CT'),
    ('DT', 'DT'),
    ('FT', 'FT'),
    ('GS', 'GS'),
    ('HBT', 'HBT'),
    ('HE', 'HE'),
    ('LBT', 'LBT'),
    ('MC', 'MC'),
    ('MG', 'MG'),
    ('MT', 'MT'),
    ('SL', 'SL'),
    ('SLT', 'SLT'),
    ('SV', 'SV'),
    ('TC', 'TC'),
    ('TH', 'TH'),
    ('VC', 'VC'),
    ('VD', 'VD'),
    ('WL', 'WL'),
    ('TL', 'TL'),
    ('AC', 'AC'),
    ('WG', 'WG'),
)

OUTGOING_TYPE = (
    ('Outgoing','Outgoing'),
    ('Transfer','Transfer'),
    ('Direct Transfer','Direct Transfer'),
)

FILE_STAT = (
    ('Documents','Documents'),
    ('Processing','Processing'),
    ('Renewed','Renewed'),
)

DELIVERY_STAT = (
    ('For Pick-Up','For Pick-Up'),
    ('Processing','Processing'),
    ('Shipped','Shipped'),
    ('Delivered','Delivered'),
    ('Received','Received'),
)

EVAL_STAT = (
    ('For Evaluation','For Evaluation'),
    ('Done','Done'),
)



ATTACH_TYPE = (
    ('Memo', 'Memo'),
    ('Warning', 'Warning'),
    ('Notice to Explain', 'Notice to Explain'),
    ('Certificate', 'Certificate'),
    ('Performance Evaluation', 'Performance Evaluation'),
    ('EDS','EDS'),
    ('License','License'),
    ('Others','Others'),
)

UNIT_ATTACH = (
    ('OR', 'OR'),
    ('CR', 'CR'),
    ('Deed of Sale', 'Deed of Sale'),
    ('Certificate', 'Certificate'),
    ('Violations', 'Violations'),
    ('Technical Specs', 'Technical Specs'),
    ('Turn Over Forms', 'Turn Over Forms'),
    ('Inspection Checklist', 'Inspection Checklist'),
    ('Transmittal Form', 'Transmittal Form'),
    ('Incident Report', 'Incident Report'),
)

CATEGORY = (
    ('Events', 'Events'),
    ('Holiday', 'Holiday'),
    ('Memo', 'Memo'),
)

FORM_TYPE = (
    ('Cash Received Slip', 'Cash Received Slip'),
    ('Cash Advance Slip', 'Cash Advance Slip'),
    ('Cash Request Slip', 'Cash Request Slip'),
    ('Cash Fund Release Slip', 'Cash Fund Release Slip'),
    ('Cash Disbursement Voucher', 'Cash Disbursement Voucher'),
    ('Liquidation Report', 'Liquidation Report'),
    ('Check Disbursement Voucher', 'Check Disbursement Voucher'),
    ('Unreceipted Form', 'Unreceipted Form'),
    ('AIP Drawings Form', 'AIP Drawings Form'),
)


WEATHER_STATUS = (
    ('Sunny', 'Sunny'),
    ('Cloudy', 'Cloudy'),
    ('Rainy', 'Rainy'),
    ('Windy', 'Windy'),
    ('Stormy', 'Stormy'),
)

TEXT_ALIGN= (
    ('caption center-align', 'caption center-align'),
    ('caption left-align', 'caption left-align'),
    ('caption right-align', 'caption right-align'),
)

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

CIVIL_STATUS = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Separated', 'Separated'),
    ('Divorced', 'Divorced'),
    ('Widowed', 'Widowed'),
    ('Ba-ak', 'Ba-ak'),
)

EMPLOYMENT_STATUS = (
    ('Active', 'Active'),
    ('Resigned', 'Resigned'),
    ('Secret', 'Secret'),
)

RELIGION = (
    ('Christianity', 'Christianity'),
    ('Pagano', 'Pagano'),
    ('Muslim', 'Muslim'),
)

EMPLOYMENT_TYPE = (
    ('Permanent', 'Permanent'),
    ('Contractual', 'Contractual'),
    ('Probationary','Probationary'),
)

RELATION = (
    ('Father', 'Father'),
    ('Mother', 'Mother'),
    ('Sibling','Sibling'),
    ('Son','Son'),
    ('Daughter','Daughter'),
    ('Wife','Wife'),
    ('Husband','Husband'),
    ('Cousin','Cousin'),
    ('Auntie','Auntie'),
    ('Uncle','Uncle'),
)

BRANCH = (
    ('Baguio', 'Baguio'),
    ('Bontoc', 'Bontoc'),
    ('Tagaytay','Tagaytay'),
)

SITES = (
    ('BMH', 'Bontoc Municipal Hall'),
    ('Contractual', 'Contractual'),
    ('Probationary','Probationary'),
)

DESIGNATION = (
    ('Driver A', 'Driver A'),
    ('Driver B', 'Driver B'),
    ('Driver C', 'Driver C'),
    ('Operator A', 'Operator A'),
    ('Operator B', 'Operator B'),
    ('Operator C', 'Operator C'),
    ('Site Checker', 'Site Checker'),
    ('Skilled Laborers', 'Skilled Laborers'),
    ('Foreman', 'Foreman'),
    ('Project Manager', 'Project Manager'),
    ('Project Engineer', 'Project Engineer'),
    ('Materials Engineer', 'Materials Engineer'),
    ('Office Engineer', 'Office Engineer'),
    ('Administrative Clerk', 'Administrative Clerk'),
    ('Head Book Keeper', 'Head Book Keeper'),
    ('Book Keeper', 'Book Keeper'),
    ('Accountant', 'Accountant'),
    ('Finance Manager', 'Finance Manager'),
    ('Head Purchaser', 'Head Purchaser'),
    ('Purchaser', 'Purchaser'),
    ('Helper 1', 'Helper 1'),
    ('Helper 2', 'Helper 2'),
    ('Helper 3', 'Helper 3'),
    ('Project In Charge', 'Project In Charge'),
    ('Liason', 'Liason'),
    ('Mechanical Engineer', 'Mechanical Engineer'),
    ('Dispatcher', 'Dispatcher'),
    ('Welder','Welder'),
    ('Inventory Analyst','Inventory Analyst'),
    ('Materials & Control Officer', 'Materials & Control Officer'),
    ('Administrative Site Supervisor', 'Administrative Site Supervisor'),
    ('Administrative Manager', 'Administrative Manager'),
    ('Assistant Equipment Manager', 'Assistant Equipment Manager'),
    ('Assistant Equipment Manager', 'Assistant Equipment Manager'),
    ('Cashier', 'Cashier'),
    ('Senior Mechanic', 'Senior Mechanic'),
    ('Chief Mechanic', 'Chief Mechanic'),
    ('Junior Mechanic', 'Junior Mechanic'),
    ('Consultant', 'Consultant'),
    ('Cook', 'Cook'),
    ('Equipment Clerk', 'Equipment Clerk'),
    ('Office Clerk', 'Office Clerk'),
    ('Equipment Manager', 'Equipment Manager'),
    ('Equipment Supervisor', 'Equipment Supervisor'),
    ('General Manager', 'General Manager'),
    ('Geodetic Engineer', 'Geodetic Engineer'),
    ('IT Junior Programer', 'IT Junior Programer'),
    ('Laborer', 'Laborer'),
    ('Liason', 'Liason'),
    ('Mechanical Engineer', 'Mechanical Engineer'),
    ('Safety Officer', 'Safety Officer'),
    ('First Aider', 'First Aider'),
    ('Security Guard', 'Security Guard'),
    ('Technical Engineer', 'Technical Engineer'),
    ('Utility', 'Utility'),
    ('Operations Manager', 'Operations Manager'),
)

TITLE = (
    ('Mr.','Mr.'),
    ('Ms.','Ms.'),
    ('Mrs.','Mrs.'),
    ('Engr.','Engr.'),
    ('Arch.','Arch.'),
)

DOC_TYPE = (
    ('Permit', 'Permit'),
    ('Certificate', 'Certificate'),
    ('License', 'License'),
)

STATUS = (
    ('Operational','Operational'),
    ('Idle','Idle'),
    ('Under Repair','Under Repair'),
    ('For Disposal','For Disposal'),
    ('Sustained','Sustained'),
)

STATUS_TRAVEL = (
    ('For Approval','For Approval'),
    ('Scheduled','Scheduled'),
    ('Travel Booked','Travel Booked'),
    ('On its way','On its way'),
    ('Arrived','Arrived'),
    ('Coming back','Coming back'),
    ('Returned','Returned'),
    ('Canceled','Canceled'),
)

STATUS_REPAIR = (
    ('For Approval','For Approval'),
    ('Under Repair','Under Repair'),
    ('For PMS', 'For PMS'),
    ('Sustained','Sustained'),
    ('Finished','Finished'),
)

APPROVAL_SUPERVISOR = (
    ('For Approval', 'For Approval'),
    ('Approved', 'Approved'),
    ('Denied', 'Denied'),
)

APPROVAL = (
    ('For Approval', 'For Approval'),
    ('Approved w/ Pay', 'Approved w/ Pay'),
    ('Approved w/o Pay', 'Approved w/o Pay'),
    ('AWOL', 'AWOL'),
    ('Denied', 'Denied'),
    ('Canceled', 'Canceled'),
)

LOAN_APPROVAL = (
    ('Approved', 'Approved'),
    ('Denied', 'Denied'),
    ('Canceled', 'Canceled'),
)


LEAVE = (
    ('Birthday Leave', 'Birthday Leave'),
    ('Sick Leave', 'Sick Leave'),
    ('Emergency Leave', 'Emergency Leave'),
    ('Vacation Leave', 'Vacation Leave'),
    ('Bereavement Leave', 'Bereavement Leave'),
    ('Paternity Leave', 'Paternity Leave'),
    ('Maternity Leave', 'Maternity Leave'),

)

PROJECT_STATUS = (
    ('For Bidding','For Bidding'),
    ('Under Construction', 'Under Construction'),
    ('Completed','Completed'),
)


PROJECT_TYPE = (
    ('Office','Office'),
    ('Project','Project'),
    ('Warehouse','Warehouse'),
    ('Project Main','Project Main'),
)


OFFICE = (
    ('Bidding', 'Bidding'),
    ('On-Site', 'On-Site'),
)

PERCENT_TYPE = (
    ('As Planned', 'As Planned'),
    ('Actual', 'Actual'),
)

WAREHOUSE_CATEGORY = (
    ('Construction Materials', 'Construction Materials'),
    ('Labor', 'Labor'),
)

ITEM_CATEGORY = (
    ('Construction Materials','Construction Materials'),
    ('Spare Parts','Spare Parts'),
    ('Oil & Lubricants','Oil & Lubricants'),
    ('PPE','PPE'),
    ('Tools & Machineries','Tools & Machineries'),
    ('Office Supply','Office Supply'),
    ('Food Supply','Food Supply'),
    ('Fuel','Fuel'),
    ('Kitchen Utensils','Kitchen Utensils'),
    ('Aggregates','Aggregates'),
    ('IT Equipment','IT Equipment'),
)

SERVICE_TYPE = (
    ('Scheduled', 'Scheduled'),
    ('Unscheduled', 'Unscheduled'),
    ('Capital Repair', 'Capital Repair'),
    ('PMS', 'PMS'),
    ('Sustained', 'Sustained'),
)

REPAIR_CAUSE = (
    ('Mishandling', 'Mishandling'),
    ('Wear & Tear', 'Wear & Tear'),
    ('Back Job', 'Back Job'),
    ('Electrical Issues', 'Electrical Issues'),
    ('PMS', 'PMS'),
    ('Others', 'Others'),
)

ORDER_STATUS = (
    ('For Approval','For Approval'),
    ('On-Process','On-Process'),
    ('Purchased','Purchased'),
    ('Canceled','Canceled'),
    ('Invalid','Invalid'),
)

TYPE_AGGREGATE = (
    ('Fine Sand','Fine Sand'),
    ('Gravel ','Gravel'),
)

WORK_ITEM = (
    ('N/A','N/A'),
    ('Active Protection System','Active Protection System'),
    ('Active Wire Mesh System (High Tensile)','Active Wire Mesh System (High Tensile)'),
    ('Aggregate Subbase Course','Aggregate Subbase Course'),
    ('Chevron Signs (450mm X 600mm)','Chevron Signs (450mm X 600mm)'),
    ('Concrete (Slope Protection)','Concrete (Slope Protection)'),
    ('Concrete Curb (Cast in Place)','Concrete Curb (Cast in Place)'),
    ('Concrete Gutter, Cast in Place','Concrete Gutter, Cast in Place'),
    ('Concrete Railing (Standard)','Concrete Railing (Standard)'),
    ('Curb and gutter, cast-in-place','Curb and gutter, cast-in-place'),
    ('Danger/Warning Signs (60 cm Triangle) W1-3','Danger/Warning Signs (60 cm Triangle) W1-3'),
    ('Detour/ Access Road','Detour/ Access Road'),
    ('Drain Pipe (Galvanized)','Drain Pipe (Galvanized)'),
    ('Drain Pipe (PVC)','Drain Pipe (PVC)'),
    ('Elastomeric Bearing Pad','Elastomeric Bearing Pad'),
    ('Erosion Control Mat (Type 4)','Erosion Control Mat (Type 4)'),
    ('Erosion Control Mat (Type I)','Erosion Control Mat (Type I)'),
    ('Expansion Joint (Rubber Multiplex)','Expansion Joint (Rubber Multiplex)'),
    ('Filter Cloth','Filter Cloth'),
    ('Forms and Falsework','Forms and Falsework'),
    ('Gabions (1mx1mx2m, Metallic Coated)','Gabions (1mx1mx2m, Metallic Coated)'),
    ('Grouted Riprap (Class A)','Grouted Riprap (Class A)'),
    ('Hand-Laid Rock Embankment','Hand-Laid Rock Embankment'),
    ('Hazard Markers (600 x 800mm)','Hazard Markers (600 x 800mm)'),
    ('Hazard Markers (Chevron Signs, 450x600mm)','Hazard Markers (Chevron Signs, 450x600mm)'),
    ('Hydroseeding','Hydroseeding'),
    ('Individual Removal of Trees (Small, 150mm - 300mm dia.)','Individual Removal of Trees (Small, 150mm - 300mm dia.)'),
    ('Individual Removal of Trees (Small, 301mm - 500mm dia.)','Individual Removal of Trees (Small, 301mm - 500mm dia.)'),
    ('Individual Removal of Trees, 501-750 mm dia','Individual Removal of Trees, 501-750 mm dia'),
    ('Inlet Type (910 mm dia.)','Inlet Type (910 mm dia.)'),
    ('Lean Concrete (class B, 16.50Mpa)','Lean Concrete (class B, 16.50Mpa)'),
    ('Metal beam end piece','Metal beam end piece'),
    ('Metal Guardrails (Metal Beam) including Concrete Post','Metal Guardrails (Metal Beam) including Concrete Post'),
    ('Occupational Safety and Health Program','Occupational Safety and Health Program'),
    ('Paint','Paint'),
    ('Passive System, Hybrid Drapery','Passive System, Hybrid Drapery'),
    ('PCCP  (Unreinforced 0.15 m thick, 14 Days)','PCCP  (Unreinforced 0.15 m thick, 14 Days)'),
    ('PCCP  (Unreinforced 0.23 m thick - 14 Days)','PCCP  (Unreinforced 0.23 m thick - 14 Days)'),
    ('PCCP (Unreinforced 0.28 m thick, 14 Days)','PCCP (Unreinforced 0.28 m thick, 14 Days)'),
    ('Permanent Ground Anchor','Permanent Ground Anchor'),
    ('Pipe Culvert (910 mm Dia., Class II)','Pipe Culvert (910 mm Dia., Class II)'),
    ('Pipe Culverts (910mm dia. Class II - RCPC)','Pipe Culverts (910mm dia. Class II - RCPC)'),
    ('Pipe Culverts 610mm diameter (24”ɸ) class II RCPC (V.O.)new item','Pipe Culverts 610mm diameter (24”ɸ) class II RCPC (V.O.)new item'),
    ('Preformed Sponge Rubber Joint Expansion','Preformed Sponge Rubber Joint Expansion'),
    ('Premolded Expansion Joint Filler with Sealant','Premolded Expansion Joint Filler with Sealant'),
    ('Project Billboard/ Signboard (For COA)','Project Billboard/ Signboard (For COA)'),
    ('Project Billboard/ Signboard (For DPWH)','Project Billboard/ Signboard (For DPWH)'),
    ('Reflectorized Pavement Studs Raised Profile Type (Bi - Directional)','Reflectorized Pavement Studs Raised Profile Type (Bi - Directional)'),
    ('Reflectorized Thermoplastic Pavement Markings White','Reflectorized Thermoplastic Pavement Markings White'),
    ('Regulatory Signs (600mm Ø, R6-4, Miscellaneous Signs, Load and Dimension Restriction Signs)','Regulatory Signs (600mm Ø, R6-4, Miscellaneous Signs, Load and Dimension Restriction Signs)'),
    ('Reinforcing Steel (Grade 40)','Reinforcing Steel (Grade 40)'),
    ('Reinforcing Steel (Grade 60)','Reinforcing Steel (Grade 60)'),
    ('Reinforcing Steel (Headwalls, Catch basins)','Reinforcing Steel (Headwalls, Catch basins)'),
    ('Relocation of Utilities (3 pcs. Electrical Post)','Relocation of Utilities (3 pcs. Electrical Post)'),
    ('Right-of-Way Monument (Precast Concrete)','Right-of-Way Monument (Precast Concrete)'),
    ('Rockfall Netting','Rockfall Netting'),
    ('Shotcrete with Reinforcing Fiber','Shotcrete with Reinforcing Fiber'),
    ('Solar LED Street Light','Solar LED Street Light'),
    ('Steel Sheet Pile (Slope Protection)','Steel Sheet Pile (Slope Protection)'),
    ('Stone masonry','Stone masonry'),
    ('Structural Concrete (Class "A" - 20.68Mpa, 28 days)','Structural Concrete (Class "A" - 20.68Mpa, 28 days)'),
    ('Structural Concrete (Class "A" - 27.56Mpa, 28 days)','Structural Concrete (Class "A" - 27.56Mpa, 28 days)'),
    ('Structural Concrete (Class "B" - 16.50Mpa, 28 days)','Structural Concrete (Class "B" - 16.50Mpa, 28 days)'),
    ('Structural Concrete (Headwalls, Catch basins)','Structural Concrete (Headwalls, Catch basins)'),
    ('Structural Concrete (Painting Works)','Structural Concrete (Painting Works)'),
    ('Structural concrete class A (minor Structure)','Structural concrete class A (minor Structure)'),
    ('Structural Concrete, Class A (Catch Basin, Headwall, RCBC)','Structural Concrete, Class A (Catch Basin, Headwall, RCBC)'),
    ('Structural concrete, class A(minor structures)','Structural concrete, class A(minor structures)'),
    ('Structural Steel, Furnished, Fabricated, and Erected (Grade 36)','Structural Steel, Furnished, Fabricated, and Erected (Grade 36)'),
    ('Warning Signs','Warning Signs'),
    ('Welded Structural Steel (Waiting Shed)','Welded Structural Steel (Waiting Shed)'),
)
