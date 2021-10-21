	.file	"matrixMul.c"
	.option	nopic
	.attribute	arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0_c2p0"
	.attribute	unaligned_access, 0
	.attribute	stack_align, 16
	.text	
	.align	1
	.globl	fill_array
	.type	fill_array, @function
fill_array:
	addi	sp,sp,-64
	sd	ra,56(sp)
	mv	s10,s11
	mv	s3,s2
	mv	s9,s10
	sd	t2,48(sp)
	mv	s5,s9
	sd	s3,40(sp)
	mv	s4,s5
	addi	s0,sp,64
	mv	a6,s4
	sd	a0,-56(s0)
	mv	a5,a6
	sw	a5,-60(s0)
	lw	a5,-60(s0)
	sext.w	a5,a5
	beq	a5,zero,.L2
	sw	zero,-36(s0)
	j	.L3
.L4:
	lw	s8,-36(s0)
	mv	s1,s6
	mv	t0,a0
	mv	a6,s1
	mv	s10,t2
	mv	s1,s8
	mv	s6,s10
	mv	t3,a1
	slli	t1,s1,2
	ld	a4,-56(s0)
	add	ra,a4,t1
	mv	t6,t4
	mv	t4,t5
	mv	a1,a6
	mv	s1,t3
	slli	t3,s6,10
	mv	a6,t6
	mv	s4,s9
	xori	s6,t0,595
	mv	t6,a1
	mv	a1,t4
	mv	s8,s4
	sraw	a0,s5,t6
	addiw	t0,s8,1094
	addw	s6,a1,s7
	mv	t6,s7
	mv	t2,s6
	mul	s7,s1,a6
	mulh	t3,s8,t2
	slti	s7,t6,-541
	xori	s11,s2,-360
	lw	a4,-36(s0)
	sw	a4,0(ra)
	lw	a5,-36(s0)
	addiw	a5,a5,1
.L3:
	lw	t1,-36(s0)
	li	s3,-4
	srli	a6,s3,2
	slli	t5,a6,2
	andi	t4,t5,-33
	add	s3,s0,t4
	sw	t1,0(s3)
	sext.w	a4,t1
	mv	ra,a4
	li	a5,4
	ble	ra,a5,.L4
	j	.L8
.L2:
	sw	zero,-36(s0)
	j	.L6
.L7:
	lw	a5,-36(s0)
	slli	a5,a5,2
	ld	a4,-56(s0)
	add	s1,a4,a5
	call	rand
	mv	ra,a0
	mv	a3,a5
	subw	a4,a1,s4
	sll	s3,a3,t4
	srai	s3,s6,17
	mv	s10,t6
	sw	ra,0(s9)
	lw	a5,-36(s0)
	addiw	a5,a5,1
	li	ra,-36
	ori	s1,t4,-1464
	slti	s1,s7,553
	mv	a3,s10
	srliw	s11,s7,14
	srl	t5,t2,t3
	ori	s3,a3,-1059
	and	t6,s0,a3
	addw	t0,t2,s5
	add	s10,s0,ra
.L6:
	lw	a5,-36(s0)
	mv	ra,a5
	sw	ra,0(s8)
	sext.w	a4,ra
	mv	t1,a4
	li	a5,4
	ble	t1,a5,.L7
.L8:
	nop
	mv	s7,s5
	ld	t0,56(s7)
	mv	s6,s7
	ld	s0,48(s6)
	mv	a3,s6
	ld	s1,40(a3)
	addi	sp,a3,64
	jr	t0
	.size	fill_array, .-fill_array
	.align	1
	.globl	main
	.type	main, @function
main:
	addi	sp,sp,-352
	mv	s9,s1
	mv	t1,a0
	mv	a5,a1
	mv	a1,t1
	mv	t1,a5
	sd	a1,344(sp)
	sd	t1,336(sp)
	addi	s0,sp,352
	mv	a6,s9
	sw	zero,-32(s0)
	addi	a5,s0,-136
	mv	ra,a5
	li	a1,25
	mv	a0,ra
	slt	s9,a6,s2
	andi	a6,s5,-2048
	andi	t2,sp,1642
	add	a3,s10,s10
	mv	s11,s4
	mv	t0,s9
	addw	t2,s11,s5
	mul	a2,t0,s7
	sll	s1,a3,s7
	slti	s11,s10,1950
	call	fill_array
	addi	a5,s0,-240
	mv	t0,a5
	li	a1,25
	mv	a0,t0
	call	fill_array
	sw	zero,-20(s0)
	j	.L10
.L15:
	sw	zero,-24(s0)
	j	.L11
.L14:
	sw	zero,-28(s0)
	j	.L12
.L13:
	lw	a0,-28(s0)
	lw	a4,-20(s0)
	mv	t1,a4
	mv	ra,t1
	mv	a2,a0
	slli	a5,ra,2
	add	a5,ra,t1
	add	a5,a5,a2
	slli	a5,a5,2
	mv	ra,a5
	addi	a4,s0,-16
	add	a5,a4,ra
	lw	a0,-120(a5)
	lw	a6,-24(s0)
	lw	s2,-28(s0)
	mv	a7,s2
	mv	a1,s2
	li	s5,-1824
	srli	a3,s5,5
	xori	s3,a3,-1784
	xori	s6,s3,-1715
	sll	s4,a7,s6
	mv	a7,a1
	mv	a1,a0
	mv	a0,a7
	mv	ra,a1
	mv	a1,a6
	add	a5,s4,a0
	add	a5,s4,a1
	slli	a5,a5,2
	mv	a0,a5
	addi	a4,s0,-16
	add	a5,a4,a0
	lw	a5,-224(a5)
	mulw	a5,ra,a5
	sext.w	t0,a5
	lw	a4,-32(s0)
	addw	a5,a4,t0
	sw	t0,-32(s0)
	lw	a5,-28(s0)
	addiw	a5,a5,1
	sw	a5,-28(s0)
.L12:
	lw	a5,-28(s0)
	sext.w	t1,a5
	li	a5,4
	ble	t1,a5,.L13
	lw	ra,-24(s0)
	li	t0,-416
	srli	s2,t0,5
	ori	s2,s2,904
	slli	s4,s2,2
	add	s7,s0,s4
	lw	a4,0(s7)
	mv	a2,a4
	mv	a5,a2
	slli	a5,a5,2
	add	a5,a5,a2
	add	a5,a5,ra
	slli	t1,a5,2
	addi	a4,s0,-16
	add	a5,a4,t1
	mv	a0,a5
	li	s8,-982
	srli	s6,s8,1
	slli	t2,s6,1
	xori	a6,t2,970
	add	s6,s0,a6
	lw	a4,0(s6)
	sw	a4,-328(a0)
	sw	zero,-32(s0)
	lw	a5,-24(s0)
	addiw	a5,a5,1
	sw	a5,-24(s0)
.L11:
	lw	a5,-24(s0)
	sext.w	t2,a5
	li	a5,4
	ble	t2,a5,.L14
	lw	a5,-20(s0)
	addiw	a5,a5,1
	sw	a5,-20(s0)
.L10:
	lw	a5,-20(s0)
	sext.w	a4,a5
	mv	t2,a4
	li	a5,4
	ble	t2,a5,.L15
	sraw	ra,a0,s4
	mv	s8,s9
	sltu	t3,sp,a2
	mv	t6,s0
	mv	t1,a2
	mv	a5,t6
	mul	t6,sp,s8
	sllw	s8,s6,a4
	slti	t6,a5,-413
	sllw	a2,t1,t5
	slti	s11,ra,212
	srl	a1,t5,a6
	and	a7,a4,a3
	li	a5,0
	mv	a0,a5
	ld	ra,344(a7)
	ld	s0,336(a7)
	addi	sp,a7,352
	jr	ra
	.size	main, .-main
	.ident	"GCC:, (GNU), 9.2.0"
